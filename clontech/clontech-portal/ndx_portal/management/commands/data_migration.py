"""
This command copies the data from the old database into the new one (sourcified)
This was necessary to upgrade ndx_auth past v1.

Tables_in_clontech:

    +------------------------------------+
    | auth_group                         |-
    | auth_group_permissions             |-
    | auth_permission                    |-
    | clontech_result_devicename         |-
    | clontech_result_result             |-
    | clontech_result_resultgeolocation  |-
    | clontech_result_resultlistcsvfile  |-
    | clontech_result_teststrip          |-
    | django_admin_log                   |- can't copy -- too complicated to determine ids
    | django_content_type                |-
    | django_migrations                  |- don't copy - obviously
    | django_session                     |- don't copy - or do?
    | ndx_audit_log_auditlog             |-
    | ndx_auth_ndxuser                   |-
    | ndx_auth_ndxuser_groups            |-
    | ndx_auth_ndxuser_user_permissions  |-
    | ndx_batch_batch                    |-
    | ndx_batch_quadraticcurveparameters |-
    | ndx_eula_eula                      |-
    | ndx_eula_eulafile                  |-
    | oauth2_provider_accesstoken        |-
    | oauth2_provider_application        |-
    | oauth2_provider_grant              |-
    | oauth2_provider_refreshtoken       |-
    +------------------------------------+

Command:

    envdir envdir ./manage.py data_migration localhost 3306 dbuser dbname /path/to/dumps/dir

Or if you have server aliases:

    django data_migration localhost 3306 dbuser dbname /path/to/dumps/dir

"""
import copy
from ndx_django_utils.data_transfer_utils import BaseDatabaseMigrationCommand
from ndx_auth.models import UserProfile
from ndx_portal.fix_group_names import fix_group_names
from ndx_result.models import Teststrip, TLine


class Command(BaseDatabaseMigrationCommand):
    help = 'Migrate data from old database to new database'

    def operations(self):
        print('Starting operations')
        self.transpose_group_user_and_permission_tables()
        self.transpose_oauth_tables()
        self.transpose_misc_tables()
        self.transpose_result_tables()
        self.migrate_to_new_tline_system()
        fix_group_names()
        print('Transfer complete')

    def _modify_values(self, legacy_record, target_records, conversions=None, convertfn=None):
        """
        Modifies the record, either using a convertfn (priority), or a set of conversions.
        This function overrides the parent class's _modify_values method so that convertfn and conversions
        are both applied - allowing the use of conversions while also modifying the record to add new fields
        """
        legacy_record = copy.deepcopy(legacy_record)
        if conversions is not None:
            for k in conversions:
                fn = conversions[k]
                if fn is None:
                    legacy_record.pop(k)
                else:
                    value = legacy_record[k]
                    legacy_record[k] = fn(value, legacy_record, target_records)
        if convertfn is not None:
            return convertfn(legacy_record, target_records)
        return legacy_record

    def __convert_ndx_user(self, legacy_record, target_records):
        legacy_record["feedback_emails"] = False
        return legacy_record

    def transpose_group_user_and_permission_tables(self):
        self.transpose('django_content_type', matchkey='model')
        self.transpose('auth_group', matchkey='name')
        self.transpose(
            'auth_permission',
            matchkey='codename',
            conversions={
                'content_type_id': self.get_mapper('django_content_type', 'content_type_id')
            })
        self.transpose(
            'auth_group_permissions',
            matchfn=self.auth_group_permission_exists,
            conversions={
                'group_id': self.get_mapper('auth_group', 'group_id'),
                'permission_id': self.get_mapper('auth_permission', 'permission_id')
            })
        self.transpose(
            'ndx_auth_ndxuser',
            legacy_pk='email',
            matchfn=self.ndx_auth_ndxuser_exists,
            convertfn=self.__convert_ndx_user,
            extra_step=self.create_profile)
        # There won't be ndxuser_groups in target db so we can just transpose ids
        self.transpose(
            'ndx_auth_ndxuser_groups',
            matchkey='id',
            preserve_id=True,
            conversions={
                'ndxuser_id': self.get_mapper('ndx_auth_ndxuser', 'ndxuser_id'),
                'group_id': self.get_mapper('auth_group', 'group_id')
            })
        # Same for ndx_auth_ndxuser_user_permissions
        self.transpose(
            'ndx_auth_ndxuser_user_permissions',
            matchkey='id',
            preserve_id=True,
            conversions={
                'ndxuser_id': self.get_mapper('ndx_auth_ndxuser', 'ndxuser_id'),
                'permission_id': self.get_mapper('auth_permission', 'permission_id')
            })
        self.transpose(
            'django_session', matchkey='session_key', legacy_pk='session_key', 
            target_pk='session_key', preserve_id=True)

    def transpose_oauth_tables(self):
        user_mapper = self.get_mapper('ndx_auth_ndxuser', 'user_id')
        self.transpose(
            'oauth2_provider_application',
            matchkey='id',
            preserve_id=True,
            conversions={
                'user_id': user_mapper
            })
        application_mapper = self.get_mapper('oauth2_provider_application', 'application_id')
        common_args = {
            'matchkey': 'id',
            'preserve_id': True,
            'conversions': {
                'user_id': user_mapper,
                'application_id': application_mapper
            }}

        # Table: oauth2_provider_accesstoken
        oauth2_provider_accesstoken_args = copy.deepcopy(common_args)
        oauth2_provider_accesstoken_args['conversions']['source_refresh_token_id'] = None
        self.transpose('oauth2_provider_accesstoken', **oauth2_provider_accesstoken_args)

        # Table oauth2_provider_grant 
        oauth2_provider_grant_args = copy.deepcopy(common_args)
        self.transpose('oauth2_provider_grant', **oauth2_provider_grant_args)

        # Table oauth2_provider_refreshtoken
        oauth2_provider_refreshtoken_args = copy.deepcopy(common_args)
        oauth2_provider_refreshtoken_args['conversions']['revoked'] = None
        self.transpose('oauth2_provider_refreshtoken', **oauth2_provider_refreshtoken_args)

    def transpose_misc_tables(self):
        self.transpose('ndx_audit_log_auditlog', matchkey='id', preserve_id=True)
        self.transpose('ndx_eula_eula', matchkey='id', preserve_id=True)
        self.transpose('ndx_eula_eulafile', matchkey='id', preserve_id=True)

    def auth_group_permission_exists(self, row, target_records):
        new_group_id = self.get_mapped_pk('auth_group', row['group_id'])
        new_permission_id = self.get_mapped_pk('auth_permission', row['permission_id'])
        for record in target_records:
            if record['group_id'] == new_group_id and record['permission_id'] == new_permission_id:
                return record

    def ndx_auth_ndxuser_exists(self, row, target_records):
        email = row['email']
        return next((record for record in target_records if record['email'] == email), None)

    def create_profile(self, legacy_record, new_pk):
        objects = UserProfile.objects
        if not objects.filter(user_id=new_pk).exists():
            objects.create(user_id=new_pk)

    def __convert_ndx_result(self, legacy_record, target_records):
        legacy_record["assay_type"] = ""
        return legacy_record

    def __convert_ndx_batch(self, legacy_record, target_records):
        legacy_record["assay_type"] = ""
        legacy_record["comments"] = ""
        legacy_record["unit"] = ""
        return legacy_record

    def transpose_result_tables(self):
        self.transpose('ndx_batch_batch', matchkey='id', preserve_id=True, convertfn=self.__convert_ndx_batch)
        self.transpose(
            'ndx_batch_quadraticcurveparameters', 
            matchkey='batch_id',
            legacy_pk='batch_id', target_pk='batch_id', preserve_id=True)
        self.transpose(
            'ndx_result_devicename',
            matchfn=self.get_matcher('make', 'model', 'display_name'),
            legacy_table='clontech_result_devicename')
        self.transpose(
            'ndx_result_result',
            matchkey='id',
            preserve_id=True,
            legacy_table='clontech_result_result',
            convertfn=self.__convert_ndx_result,
            conversions={
                'batch_id': self.get_mapper('ndx_batch_batch', 'batch_id'),
                'created_by_id': self.get_mapper('ndx_auth_ndxuser', 'created_by_id')
            })
        self.transpose(
            'ndx_result_resultgeolocation',
            matchkey='result_id',
            target_pk='result_id',
            legacy_pk='result_id',
            preserve_id=True,
            legacy_table='clontech_result_resultgeolocation',
            conversions={
                'result_id': self.get_mapper('ndx_result_result', 'result_id')
            })

        self.teststrip_lost_data = {}

        def teststrip_extra_step(legacy_record, new_pk):
            """
            We are dropping fields from teststrip which we need to bring into Tlines.
            So let's capture them in a dict
            """
            self.teststrip_lost_data[new_pk] = {
                't_c_ratio': legacy_record['t_c_ratio'],
                'tline_peak_position': legacy_record['tline_peak_position'],
                'tline_score': legacy_record['tline_score']
            }

        self.transpose(
            'ndx_result_teststrip',
            matchkey='id',
            preserve_id=True,
            legacy_table='clontech_result_teststrip',
            extra_step=teststrip_extra_step,
            conversions={
                'result_id': self.get_mapper('ndx_result_result', 'result_id'),
                't_c_ratio': None,
                'tline_peak_position': None,
                'tline_score': None
            })
        self.transpose(
            'ndx_result_resultlistcsvfile',
            matchkey='id',
            preserve_id=True,
            legacy_table='clontech_result_resultlistcsvfile',
            conversions={
                'user_id': self.get_mapper('ndx_auth_ndxuser', 'user_id')
            })

    def migrate_to_new_tline_system(self):
        """
        This is form upgrade to version 5.1.0 of portal apps, where we move to related
        Tlines model.
        """
        for teststrip in Teststrip.objects.all():
            lost_data = self.teststrip_lost_data[teststrip.id]
            TLine.objects.create(
                teststrip=teststrip,
                score=lost_data['tline_score'],
                peak_position=lost_data['tline_peak_position'],
                t_c_ratio=lost_data['t_c_ratio']
            )
