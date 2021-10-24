# open both files
with open('gunicorn-systemd.template.service', 'r') as firstfile, open('/etc/nginx/sites-available/%s.conf', 'a' % site_name) as secondfile:
    # read content from first file
    for line in firstfile:
        # write content to second file
        secondfile.write(line)