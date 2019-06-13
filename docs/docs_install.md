# Installation

Install dependencies:
```
apt-get install git python3-pip apache2 libapache2-mod-wsgi-py3 libpq-dev
```

Create a user and group to run the app.
```
addgroup --system capstone
adduser --system --ingroup capstone capstone
```

Clone the app.
```
git clone https://github.com/capstoneteamb/capstone360.git /opt/capstone360
```

Create a config file at `/etc/capstone.prod.cfg` with any flask settings you want to override. Example:
```
DEBUG = False
SECRET_KEY = 'generate something with os.urandom()'
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://user:pass@host/db'
```

Point an Apache vhost at the app's WSGI file.
```
<VirtualHost *:80>
    ServerName capstone360.cs.pdx.edu

    WSGIDaemonProcess app user=capstone group=capstone threads=2
    WSGIScriptAlias / /opt/capstone360/app.wsgi

    <Directory /opt/capstone360>
        WSGIProcessGroup app
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
</VirtualHost>
```

Restart Apache to start running the app.
```
service apache2 restart
```
