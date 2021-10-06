from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/jdotb/superlists.git'
user = env.user
host = env.host


def deploy():
    site_folder = '/home/' + env.user + '/sites/' + env.host
    source_folder = site_folder + '/source3'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('db', 'static', 'virtualenv', 'source3'):
        run('mkdir -p ' + site_folder + '/' + subfolder)


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd ' + source_folder + ' && git fetch')
    else:
        run('git clone ' + REPO_URL + ' '+source_folder)
    current_commit = run('git log -n 1 --format=%H')
    run('cd ' + source_folder + ' && git reset --hard ' + current_commit)


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["' + site_name + '"]'
        )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, 'SECRET_KEY = "' + key + '"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('python3.9 -m venv ' + virtualenv_folder)
    run(virtualenv_folder + '/bin/pip install -r ' + source_folder + '/requirements.txt')


def _update_static_files(source_folder):
    run(
        'cd ' + source_folder + ' && ../virtualenv/bin/python manage.py collectstatic --noinput'
    )


def _update_database(source_folder):
    run(
        'cd ' + source_folder + ' && ../virtualenv/bin/python manage.py migrate --noinput'
    )
