from ndx_result_source.models.result_list_csv_file import *  # noqa
import ndx_result_source.models.result_list_csv_file as source  # noqa


class ResultListCsvFile(source.ResultListCsvFile):
    """
    This is the old and inefficient method of CSV generation, we don't use this anymore (see ndx_result/api_views.py 
    for what we do use), but we're leaving this skeleton in for shadow apps compatibility.
    """
    pass
