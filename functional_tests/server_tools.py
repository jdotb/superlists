from os import path
import subprocess
# from fabric.api import run
# from fabric.context_managers import settings

THIS_FOLDER = path.dirname(path.abspath(__file__))


# def _get_manage_dot_py(host):
#     return f'~/sites/{host}/virtualenv/bin/python ~/sites/{host}/source/manage.py'

def reset_database(host):
    subprocess.check_call(
        ['fab', 'reset_database', '--host=gametime@{}'.format(host)],
        cwd=THIS_FOLDER
    )


def create_session_on_server(host, email):
    return subprocess.check_output(
        [
            'fab',
            'create_session_on_server:email={}'.format(email),
            '--host=gametime@{}'.format(host),
            '--hide=everything,status',
        ],
        cwd=THIS_FOLDER
    ).decode().strip()
