from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from .models import db

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
    from .commands import create_db, drop_db, add_user, poll_stats

    app.cli.add_command(create_db)    
    app.cli.add_command(drop_db) 
    app.cli.add_command(add_user)
    app.cli.add_command(poll_stats)
    
    return app

