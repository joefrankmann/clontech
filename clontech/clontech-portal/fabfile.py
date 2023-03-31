"""
DO NOT MODIFY THIS FILE - SEE BELOW.

Overview:
---------

This module defines the commands for fabric, which you run like so:

    fab deploy -env staging

With arguments:

    fab deploy -env staging

With arguments (shorthand):

    fab deploy -e staging

See shadow apps readme for list of commands and their usage.

Customisations:
---------------

This file is copied from a template in ndx_django_utils and must not be modified (or ndx_frontend 
unit tests will fail).

Create a file called fabric_customisations.py (which this module imports from) and put customisations
and extra commands in there.

See ndx_django_utils/deployment/fabric_customisations_example.py

We do this so we can ensure that each portal's fabfile:

    a) Contains the same commands (some of which are used in CI)
    b) Uses the Base Deployer classes


Troubleshooting:
----------------

You may need to:

    pip install fabric

Fabric commands run via ssh on the target server, using the local copy of this file, but 
deployments likely check out code from repositories (thereby installing the remote files, not local copies).

If you get the error "No idea what 'xyz' is!" it means fabric could not find a command or argument.
Command name matches the name of the function, but fabric changes underscores (_) to hyphens (-) in
command name as well as arguments.

Do not create new commands with names likely to be used as a variable for another command (e.g. develop) as 
fabric will get confused!
"""

from invoke.tasks import task

# We use * + noqa so that we can import portal-specific commands.
from fabfile_custom import *  # noqa
from invoke.exceptions import Exit
from ndx_django_utils.deployment.misc_commands import *  # noqa


@task(
    optional=('env', 'branch', 'version', 'skip', 'prompt'), 
    help={
        'env': 'The server environment to deploy to (shadow, staging, prelive, live).',
        'branch': 'The git branch to deploy.',
        'skip': 'Instruction to skip steps for quicker runs when you know what has changed.\
                Use any combination of "npcm" to skip npm, pip, collectstatic and migrations respectively.',
        'version': 'The version of this deployment, for live & prelive only.',
        'prompt': 'Whether to prompt to check details before proceeding. Defaults to true.'
    })
def deploy(context, env=None, branch=None, version=None, prompt=True, skip=''):
    """
    Deploys to a server using default branch for that server if none is specified. 
    Live and Prelive require a release version too e.g. v1.0.0
    
    You can skip any of these steps:
        npm
        pip
        collectstatic
        migrations
    By including the first letter in the string arg to skip. E.g.

        fab deploy staging -s cm

    Will skip collectstatic and migrations.
    """
    deployer_classes = {
        'shadow': Shadow,  # noqa
        'staging': Staging,  # noqa
        'prelive': Prelive,  # noqa
        'live': Live  # noqa
    }
    default_branches = {
        'shadow': 'shadow',
        'staging': 'alpha',
        'prelive': 'beta',
        'live': 'master'
    }
    if env not in deployer_classes:
        valid_env_values = ', '.join(deployer_classes.keys())
        raise Exit('You must provide parameter "env" as one of: {}'.format(valid_env_values))
    if branch is None:
        branch = default_branches[env]
    deployer = deployer_classes[env](branch=branch, prompt=prompt, skip=skip, version=version)
    deployer.deploy()
