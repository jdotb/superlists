import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/jdotb/superlists.git'


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()


def _get_latest_source(source_folder):
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')


def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):
        run(f'python3.7 -m venv virtualenv')
    run('./virtualenv/bin/pip install -r requirements.txt')


def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')


def _update_static_files():
    run('./virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database():
    run('./virtualenv/bin/python manage.py migrate --noinput')


"""
PROVISION NGINX AND GUNICORN

[STEP 1]
1. Use cat to print file
2. Use sed to sub DOMAIN for name of site
3. Pipe output to (sudo) tee to write to nginx 'sites-available'

        cat ./deploy_tools/nginx.template.conf \
            | sed "s/DOMAIN/superlists.jdotbdotb.com/g" \
            | sudo tee /etc/nginx/sites-available/superlists.jdotbdotb.com
            
[STEP 2]

* Activate with symlink

        sudo ln -s /etc/nginx/sites-available/superlists.jdotbdotb.com\
            /etc/nginx/sites-enabled/superlists.jdotbdotb.com
            
[STEP 3]

* Write systemd service using sed

        cat ./deploy_tools/gunicorn-systemd.template.service \
            | sed "s/DOMAIN/superlists.jdotbdotb.com/g" \
            | sudo tee /etc/systemd/system/gunicorn-superlists.jdotbdotb.com.service
            
[STEP 4]

* start all services

        sudo systemctl daemon-reload $$ sudo systemctl reload nginx && sudo systemctl enable 
        gunicorn-superlists.jdotbdotb.com && sudo systemctl start gunicorn-superlists.jdotbdotb.com 

"""
