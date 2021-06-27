from poll.forms import LoginForm
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user

from . import db
from .models import User
from .forms import LoginForm


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():  # we don't have to check whether it is a POST request, validate_on_submit does this
        secret_key = str(form.secret_key.data)

        user = User.query.filter_by(secret_key=secret_key).first()

        print(user)

        if not user:
            flash("Deze code is niet geldig, probeer opnieuw...")
            return redirect(url_for("auth.login"))

        # if the above check passes, then we know the user has the right credentials
        login_user(user)
        # proceed to main
        return redirect(url_for("main.poll"))  

    # get
    return render_template("login.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

