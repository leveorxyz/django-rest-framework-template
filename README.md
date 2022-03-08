# Django-rest-framework-template

The is a Django rest framework template.

## Project Directory Structure

```bash

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
