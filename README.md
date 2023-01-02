# MLCenter
[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)



<img src="https://raw.githubusercontent.com/mlcenter-org/mlcenter-server/main/mlcenter/static/brand/logo_square.png" width="28" /> [![Website](https://img.shields.io/badge/Website-cccccc?style=for-the-badge&logo=web&logoColor=white)](https://mlcenter.org)


Governance-Driven MLOps Platform

## About

MLCenter is an Open Source MLOps Platform aiming to simplify tracking and promotion of Machine Learning models across different lifecycles.

The application is built using [Cookiecutter Django](https://github.com/cookiecutter/cookiecutter-django) and [Django](https://www.djangoproject.com/).

To interact with the MLCenter Server you can use the mlcenter python package which is available on [GitHub](https://github.com/mlcenter-org/mlcenter) and soon on [PyPi](https://pypi.org/project/mlcenter/).

To learn more about the project, please visit the [website](https://mlcenter.org).


## Getting Started

### ENV FILES


#### .env for local development

```bash
USE_DOCKER=yes
IPYTHONDIR=/app/.ipython
DATABASE_URL=postgres://debug:debug@mlcenter_local_postgres:5432/mlcenter

# if you leave MLCENTER_USE_S3 as False it will use the local file system however it is not persistent
# If you do not want to use S3 but still look to persist data you can mount a volume to `/app/mlcenter/media` in the docker container. This will allow you to persist data between container restarts.
MLCENTER_USE_S3=False
AWS_S3_REGION_NAME=""
AWS_S3_ENDPOINT_URL=""
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
AWS_STORAGE_BUCKET_NAME=""
```

#### .env for production environment

```bash
DJANGO_SETTINGS_MODULE="config.settings.production"
DJANGO_SECRET_KEY=""
DATABASE_URL=postgres://debug:debug@mlcenter_local_postgres:5432/mlcenter
DJANGO_ALLOWED_HOSTS=["*"] # here you should add your domain name
# something hard to guess unless you're happy with the default
DJANGO_ADMIN_URL="admin/"

# TIP: better off using DNS, however, redirect is OK too
DJANGO_SECURE_SSL_REDIRECT=False
DJANGO_SERVER_EMAIL=
WEB_CONCURRENCY=4
REDIS_URL=redis://redis:6379/0

MLCENTER_USE_S3=False
AWS_S3_REGION_NAME=""
AWS_S3_ENDPOINT_URL=""
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
AWS_STORAGE_BUCKET_NAME=""

# uncomment out the following line if you want to use an EMAIL SERVER otherwise use logs to get emails (activation link will show up in the logs)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'youremail@gmail.com'
# EMAIL_HOST_PASSWORD = 'email_password'
# EMAIL_PORT = 587
```

You can try using the public min.io for testing -- DO NOT USE THIS IN PRODUCTION (credentials are public)

```bash
MLCENTER_USE_S3=True
AWS_S3_REGION_NAME=""
AWS_S3_ENDPOINT_URL="https://play.min.io/mlcenter"
AWS_ACCESS_KEY_ID="Q3AM3UQ867SPQQA43P2F"
AWS_SECRET_ACCESS_KEY="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG"
AWS_STORAGE_BUCKET_NAME="mlcenter"
```



### Spin up the development server

    $ docker-compose -f local.yml up -d

### Spin up the production server

    $ docker-compose -f production.yml up -d

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

-   To create a **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).


# License

License: MIT

# Contributors

- cristianexer:  [GitHub](https://github.com/cristianexer) | [LinkedIn](https://www.linkedin.com/in/cristianexer/)