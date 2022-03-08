#!/bin/bash

source venv/bin/activate
rm -rf db.sqlite3

find . -path "*migrations*" -name "*.py" -not -path "*__init__*" -not -path "./venv?*" -delete

# mysql -u admin -p -e 'drop database db_name'
# mysql -u admin -p -e 'create database db_name'


python manage.py makemigrations
python manage.py migrate --run-syncdb --database default
python manage.py makesuper
# python manage.py loaddata db_backup.json
python manage.py runserver
