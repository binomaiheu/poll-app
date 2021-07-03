import os

import click
from flask import Flask
from flask_login import LoginManager
from flask.cli import load_dotenv, with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Voer eerst je geheime code in !'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)


    # protect the app from CORS attacks, 
    # https://testdriven.io/blog/csrf-flask/
    # Now, by default, all POST, PUT, PATCH, and DELETE methods are protected against CSRF. 
    # Take note of this. You should never perform a side effect, like changing data in the database, via a GET request.
    # all forms should includ e: 
    # <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"> ? probably unless created with WTF-Forms

    csrf = CSRFProtect()
    csrf.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))


    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # adding the cli 
    app.cli.add_command(create_db)    
    app.cli.add_command(drop_db) 

    return app


@click.command('createdb')
@with_appcontext
def create_db():
    """
    Command to initilize the database
    """

    # Need to import those here and not at the top otherwise we get circular import errors
    from .models import User, Vote, Option
    from .tools import key_gen

    db.create_all()

    # Confugration
    option_list = {
        "Functies": [
            "Ontmoetingsplaats voor jong en oud",
            "Groenzone, nadruk op bomen, struiken, vegetatie",
            "Sportterrein",
            "Zone om activiteiten te organiseren met de wijk",
            "Speeltuin / avontuurlijke zone voor de kinderen"
        ],
        "Elementen": [
            "Trampoline / springkussen ingewerkt in de grond",
            "Petanquebaan",
            "Bomen",
            "Fruitbomen",
            "Notenbomen",
            "Voetbal pleintje met doeltjes",
            "Fietsdraaimolen",
            "Deadride zoals achter gemeentehuis in Destelbergen",
            "Basketbal goal",
            "Grillplaats",
            "Heuveltje als speels landschapselement",
            "Tennis terrein",
            "Padel terrein",
            "Schommels",
            "Wipplank",
            "Zandbak",
            "Blote voetenpad",
            "Pluktuin met bessenstruken, rabarber, e.d.",
            "Bloemenweide voor de bijtjes",
            "Zwemvijver",
            "Electriciteit en watervoorziening om activiteiten te kunnen organiseren",
            "Workout toestellen voor adolescenten en volwassenen",
            "Schommelbank voor ouderen of mindervaliden",
            "Hangmatten",
            "Zitbanken",
            "Picnic tafels",
            "Levensgroot schaakspel",
            "Lage boomhut",
            "Atletiek oefenplein zoals vb. Kogelstoten, speerwerpen",
            "Open stuk met enkel gras voor activiteiten"
        ]
    }

    num_users = 20

    # different options
    functions = [ Option(description=option_list["Functies"][i], category="Functies") for i in range(len(option_list["Functies"])) ]
    elements = [ Option(description=option_list["Elementen"][i], category="Elementen") for i in range(len(option_list["Elementen"])) ]


    # generate list of num_users users with random secret key
    users = [ User(secret_key=key_gen(), weight=1.) for i in range(num_users) ]


    # insert in the database
    db.create_all()
    db.session.bulk_save_objects(functions)
    db.session.bulk_save_objects(elements)
    db.session.bulk_save_objects(users)

    db.session.commit()

    # now generate the votes
    # query the whole list to get the id's from the database & reset the score for all 
    users = User.query.all()
    options = Option.query.all()
    for u in users:
        for q in options:
            v = Vote(user_id=u.id, option_id=q.id, score=0)
            db.session.add(v)

    db.session.commit()


@click.command('dropdb')
@with_appcontext
def drop_db():
    db.drop_all()
