Provisioning a new site
=======================

## Required packages:
* nginx
* Python 3.9
* virtualenv + pip
* Git

* eg, on Ubuntu:
    > sudo add-apt-repository ppa:fkrull/deadsnakes

    > sudo apt-get install nginx git python39 python3.9-venv

## Nginx Virtual Host config
* see nginx.template.conf
* replace SITENAME with, e.g., staging.my-domain.com

## Systemd service
1. Add a new service with this command:
    > **sudo nano /etc/systemd/system/gunicorn-SITENAME.service**

    a. add the config file using *gunicorn-systemd.template*


2. Load the new service:
    > **sudo systemctl daemon-reload**

3. Tell Systemd to always load service on boot:
    > **sudo systemctl enable gunicorn-SITENAME**

4. Start the service:
    > **sudo systemctl start gunicorn-SITENAME**

    i. see *gunicorn-systemd.template.service*

    ii. replace SITENAME with the site's name, e.g., stage.my-domain.com


* NOTE: for debugging...
  > **sudo journalctl -u gunicorn-SITENAME**
* ask Systemd to check validity of service config:
  > **systemd-analyze verify /path/to/my.service**
## Folder structure:
Assume we have a user account at /home/username:

    /home/username
    └── sites
        └── SITENAME
            ├── database
            ├── source
            ├── static
            └── virtualenv