=====================
django-admin-honeypot
=====================

# Project description

**django-admin-honeypot** is a fake Django admin login screen to log and notify
admins of attempted unauthorized access. This app was inspired by discussion
in and around Paul McMillan's security talk at DjangoCon 2011.

- **Author**: `Derek Payton <http://dmpayton.com/>`\_
- **Contributor**: `Kalyaan Singh`
- **Version**: 1.2.0
- **License**: MIT

# Documentation

http://django-admin-honeypot.readthedocs.io

## tl;dr

1.  Install django-admin-honeypot from PyPI::

        pip install django-admin-honeypot

2.  Add `admin_honeypot` to `INSTALLED_APPS` setting like this
    ::

          INSTALLED_APPS = [
          ...
          'admin_honeypot',
          ]

3.  Update your urls.py:
    ::

            urlpatterns =[

            path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
            path('secret/', admin.site.urls),
            ...
            ]

4.  [ Optional ] In settings.py:
    ::

        # To receive email notifications regarding attempts to login to the admin honeypot.

        # Admin's name and email to send email
                ADMINS = (
                (admin_name, admin_email_addrress)
                )

        # SMTP CONFIGURATION
                EMAIL_HOST = smtp.gmail.com
                EMAIL_PORT = 587
                EMAIL_HOST_USER = admin_email_addrress
                EMAIL_HOST_PASSWORD = admin_email_addrress_password
                EMAIL_USE_TLS = True

5.  Run `python manage.py migrate` to create the LoginAttempt model

NOTE: replace `secret` in the url above with your own secret url prefix
