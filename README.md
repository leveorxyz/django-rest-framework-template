# Django-rest-framework-template

The is a Django rest framework template.

## Project Directory Structure

```bash
.
├── core
│   ├── admin.py
│   ├── apps.py
│   ├── classes.py
│   ├── exceptions.py
│   ├── __init__.py
│   ├── literals.py
│   ├── management
│   │   └── commands
│   │       └── makesuper.py
│   ├── migrations
│   │   └── __init__.py
│   ├── mixins.py
│   ├── models.py
│   ├── modelutils.py
│   ├── pagination.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── utils.py
│   └── views.py
├── Django_rest_framework_template
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── example.env
├── manage.py
├── README.md
├── requirements.txt
├── scripts
│   ├── deploy.sh
│   └── fresh_init.sh
├── templates
│   └── email
│       ├── account_verification.html
│       └── password_reset.html
└── user
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── migrations
    │   ├── 0001_initial.py
    │   └── __init__.py
    ├── models.py
    ├── serializers.py
    ├── tests.py
    ├── urls.py
    ├── utils.py
    └── views.py

10 directories, 42 files

```

## Requirements

See the requirements for this project on requirements.txt file.

## Installation

- Go to the repository and create a virtual environment.

```bash
python3 -m venv venv
```

- Activate the virtual environment and install dependencies.

```bash
source venv/bin/activate
pip install -r requirements.txt
```

- Then install wheel, build-essential, python3-dev and psycopg2

```bash
pip install wheel
sudo apt install build-essential
sudo apt install python3-dev
pip install psycopg2
```

- Copy the `example.env` file to `.env` and fill in the values.

```bash
cp example.env .env
```

- The `.env` file should look like this:

```text
SECRET_KEY=<key>
VERSION=v1
DEBUG=True
EMAIL_HOST_USER=acd@gmail.com
EMAIL_HOST_PASSWORD=abcd
BACKEND_URL=<backend url>
FERNET_KEY=<key>
FRONTEND_URL=<frontend url>
BRANCH=dev
```

- Create and migrate the database.

```bash
python manage.py migrate
```

## Running the server

- You can run the server with the following command:

```bash
python manage.py runserver
```

- You can also run the server on a custom port by adding the port number after the `runserver` command:

```bash
python manage.py runserver 8000
```
