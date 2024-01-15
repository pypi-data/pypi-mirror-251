# django-db-email

Database email backend for Django.

## Rationale

Capture emails in database during development.

## Support

Supports: Python 3.10.

Supports Django Versions: 4.2.7

## Installation

```shell
$ pip install django-db-email
```

## Usage

Add `db_email` to `INSTALLED_APPS`.

Set `EMAIL_BACKEND` to: "db_email.backend.EmailBackend"

Run migrations:

```shell
python manage.py migrate
```

View captured emails in Django Admin.