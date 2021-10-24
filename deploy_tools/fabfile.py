from fabric.contrib.files import *
from fabric.api import env, local, cd, run, sudo, warn_only
import random
import getpass
import shutil

REPO_URL = 'https://github.com/jdotb/superlists.git'
systemd_folder = '/etc/'
user = env.user
host = env.host
env.colorize_errors = 'true'


def _get_base_folder(host):
    return '~/sites/' + host


def _get_manage_dot_py(host):
    return '{path}/virtualenv/bin/python {path}/source/manage.py'.format(
        path=_get_base_folder(host)
    )


def reset_database():
    run('{manage_py} flush --noinput'.format(
        manage_py=_get_manage_dot_py(env.host)
    ))


# Creates session in db - if running locally, call directly.
# If running against the server, need to make a few hops:
#    - use subprocess to get to Fabric using 'fab'
#    - 'fab' lets us run management command that calls the same function on the server
def create_session_on_server(email):
    session_key = run('{manage_py} create_session {email}'.format(
        manage_py=_get_manage_dot_py(env.host),
        email=email,
    ))
    print(session_key)


def deploy():
    site_folder = '/home/' + env.user + '/sites/' + env.host
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder, site_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def config_services():
    site_folder = '/home/' + env.user + '/sites/' + env.host
    source_folder = site_folder + '/source'
    SITENAME = env.host
    nginx_template = source_folder + '/deploy_tools/nginx.template.conf'
    gunicorn_template = source_folder + '/deploy_tools/guinicorn-systemd.template.service'
    _configure_nginx(SITENAME)
    _add_gunicorn_service(gunicorn_template, SITENAME)
    _start_services(SITENAME)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('db', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % source_folder)
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, 'DOMAIN = "127.0.01"', 'DOMAIN = "%s"' % (site_name,))
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % key)
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')
    print("Settings updated, moving to update virtualenv")


def _update_virtualenv(source_folder, site_folder):
    virtualenv_folder = site_folder + '/virtualenv'
    print("virtualenv folder: " + virtualenv_folder)
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % virtualenv_folder)
    run('%s/bin/pip install -r %s/requirements.txt' % (
        virtualenv_folder, source_folder
    ))


def _update_static_files(source_folder):
    with cd(source_folder):
        run('../virtualenv/bin/python3 manage.py collectstatic --noinput')


def _update_database(source_folder):
    with cd(source_folder):
        run('../virtualenv/bin/python3 manage.py migrate --noinput')


def _configure_nginx(SITENAME):
    # sed s/replaceme/withthis/g
    sudo("ln -s /etc/nginx/sites-available/%s /etc/nginx/sites-enabled/%s" % (SITENAME, SITENAME))


def _add_gunicorn_service(gunicorn_template, SITENAME):
    run('sed s/%s/%s/g %s | sudo tee etc/init/gunicorn-%s.conf' % (SITENAME, SITENAME, gunicorn_template, SITENAME))


def _start_services(SITENAME):
    run('sudo systemctl reload nginx && sudo start gunicorn-%s' % SITENAME)
