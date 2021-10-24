import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run, sudo

REPO_URL = 'https://github.com/jdotb/superlists.git'


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    superlists_folder = source_folder + '/superlists'

    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_virtualenv(site_folder, superlists_folder)
    _create_or_update_dotenv()
    with cd(superlists_folder):
        _update_static_files()
        _update_database()


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('db', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')
    print("Directory structure made successfully, now lets get our source files.")


def _get_latest_source(source_folder):
    print("Beginning source discovery: Do we have a .git file?")
    superlists_folder = source_folder + '/superlists'
    # Check for .git in source folder, if exists, fetch latest source
    if exists(superlists_folder + '/.git'):
        print(".git found! - let's fetch the source")
        with cd(source_folder):
            run('git fetch')

    # If no .git file found, clone the repo
    else:
        print(f"No .git found inside {superlists_folder} - let's clone the repo")
        with cd(source_folder):
            run(f'git clone {REPO_URL}')

    # Capture current commit from local machine
    current_commit = local("git log -n 1 --format=%H", capture=True)
    with cd(superlists_folder):
        run(f'git reset --hard {current_commit}')


def _update_virtualenv(site_folder, superlists_folder):
    print("Virtual environment setup start...")
    if not exists(f'{site_folder}/virtualenv/bin/pip'):
        sudo("apt-get install python3.8-venv -y")
        run(f'python3.8 -m venv {site_folder}/virtualenv')
    with cd(superlists_folder):
        run(f'{site_folder}/virtualenv/bin/pip install -r requirements.txt')


def _create_or_update_dotenv():
    print("Begin env setup...")
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    print("removed django_debug")
    append('.env', f'SITENAME={env.host}')
    print(f"set SITENAME to {env.host}")
    current_contents = run('cat .env')
    print("Checking for DJANGO_SECRET_KEY...")
    if 'DJANGO_SECRET_KEY' not in current_contents:
        print("No secret key found...making one...")
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')
        print("Added secret key to django")


def _update_static_files():
    print("Updating static files...")
    run('../../virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database():
    print("Updating db")
    run('../../virtualenv/bin/python manage.py migrate --noinput')


"""
PROVISION NGINX AND GUNICORN

[STEP 1]
1. Use cat to print file
2. Use sed to sub DOMAIN for name of site
3. Pipe output to (sudo) tee to write to nginx 'sites-available'

        cat ./deploy_tools/nginx.template.conf \
            | sed "s/DOMAIN/superlists-staging.jdotbdotb.com/g" \
            | sudo tee /etc/nginx/sites-available/superlists-staging.jdotbdotb.com
            
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
