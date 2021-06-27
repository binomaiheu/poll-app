from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_login.utils import _secret_key
from . import db
from .forms import PollForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/poll', methods=['GET', 'POST'])
@login_required
def poll(): 

    # https://prettyprinted.com/tutorials/how-to-use-fieldlist-in-flask-wtf
   

    titles = [
        "Idea 1",
        "Idea 2",
        "Idea 3"
    ]


    form = PollForm(questions=[ 
        {"rating": 5 },
        {"rating": 3 },
        {"rating": 0 } ])
   
    print("about to validate... ")

    if form.validate_on_submit():  # we don't have to check whether it is a POST request, validate_on_submit does this
        print("here !!")
        for rating in form.questions.data:
            print(rating)

        # here redirect to "thank you page" return redirect(url_for("main.poll"))  

    print(form.questions)
    print(form.errors)

    return render_template(
        'poll.html',
        secret_key=current_user.secret_key, 
        titles=titles,    
        form=form)

