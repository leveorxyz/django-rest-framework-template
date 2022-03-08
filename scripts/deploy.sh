export $(grep -v '^#' .env | xargs)

source venv/bin/activate
git pull origin $BRANCH
pip install -r requirements.txt
python manage.py migrate
supervisorctl restart all