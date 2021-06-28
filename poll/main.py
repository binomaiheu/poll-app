from flask import Blueprint, render_template
from flask.helpers import url_for
from flask_login import login_required, current_user, logout_user
from flask_login.utils import _secret_key
from werkzeug.utils import redirect
from . import db
from .forms import PollForm
from .tools import get_user_scores

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/poll', methods=['GET', 'POST'])
@login_required
def poll(): 

    # https://prettyprinted.com/tutorials/how-to-use-fieldlist-in-flask-wtf
   
    # get the scores given by the user to each option
    result = get_user_scores( current_user.secret_key )

    votes = [ x[1] for x in result ]

    form = PollForm(questions=[{"rating": x.score } for x in votes ])
    titles = [ x[0].description for x in result ]

    if form.validate_on_submit():  # we don't have to check whether it is a POST request, validate_on_submit does this

        for idx, q in enumerate(form.questions):
            # put the scores back into the database and go to thank you page...
            votes[idx].score = q.rating.data
            
            # add to the session
            db.session.add(votes[idx])
        
        # and persist to database
        db.session.commit()
        
        # set voted flag
        current_user.has_voted = True
        db.session.add(current_user)
        db.session.commit()

        return redirect(url_for('main.success'))

    #print(form.questions)
    #print(form.errors)

    return render_template(
        'poll.html',
        secret_key=current_user.secret_key, 
        titles=titles,    
        form=form)


@main.route('/success')
@login_required
def success():
    logout_user()
    return render_template('success.html')
