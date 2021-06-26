from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user

from . import db
from .models import User


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        secret_key = request.form.get('secret_key')

        user = User.query.filter_by(secret_key=secret_key).first()

        print(user)

        if not user:
            flash("Deze code is niet geldig, probeer opnieuw...")
            return redirect(url_for("auth.login"))

        # if the above check passes, then we know the user has the right credentials
        login_user(user)
        # proceed to main
        return redirect(url_for("main.profile"))

    # get
    return render_template("login.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

