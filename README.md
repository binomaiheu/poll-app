# poll-app

A simple polling app with a back-end database for getting some citizen feedback on the development of a nature zone in our street. 

Some links : 

* stylesheet using bulma : https://bulma.io/documentation/
* flask tutorial by m$ : https://docs.microsoft.com/en-us/visualstudio/python/learn-flask-visual-studio-step-03-serve-static-files-add-pages?view=vs-2017



## gunicorn

```
$ gunicorn -c gunicorn_config.py "poll:create_app()"
```


## bootstrapping

We defined a number of CLI interfaces for managing the database : 

To create & fill the db with empty scores

```
flask createdb
```

To remove all the tables : 

```
flask dropdb
```

## Configuration

Create .env file with :

```
FLASK_APP=poll
FLASK_ENV=development

SECRET_KEY=123456

SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_DATABASE_URI="sqlite:///poll.db"
```

## Deploying
apt update
apt upgrade
apt install libpq-dev
python -m venv venv
./venv/bin/activate
pip install -r requirements.txt

