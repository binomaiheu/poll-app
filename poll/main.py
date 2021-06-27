from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_login.utils import _secret_key
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/poll')
@login_required
def poll():    
    return render_template(
        'poll.html',
        secret_key=current_user.secret_key)

