# Server configuration
The app is cloned at `/opt/capstone360`. The app runs as the `capstone` user, permissions should be set accordingly.

Apache configuration is in `/etc/apache2/sites-enabled/000-capstone.conf`.

App configuration can be found in `/etc/capstone.prod.cfg`. This uses the flask config file format, and any flask settings that need to be overridden can be set here. This includes the database credentials.
