from flask import Blueprint, render_template, flash
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
   
    # get the scores given by the user to each option, this returns a list of 
    # tuples containing the (Option, Vote) for the query
    result = get_user_scores( current_user.secret_key )

    votes_functions = [ x[1] for x in result if x[0].category == "Functies" ]
    votes_elements  = [ x[1] for x in result if x[0].category == "Elementen" ]

    titles_functions = [ x[0].description for x in result if x[0].category == "Functies" ]
    titles_elements = [ x[0].description for x in result if x[0].category == "Elementen"]

    form = PollForm(functions=[{"rating": v.score } for v in votes_functions ],
                    elements=[{"rating": v.score } for v in votes_elements ])
    

    if form.validate_on_submit():  # we don't have to check whether it is a POST request, validate_on_submit does this

        for idx, q in enumerate(form.functions):
            # put the scores back into the database and go to thank you page...
            votes_functions[idx].score = q.rating.data
            db.session.add(votes_functions[idx])
        
        for idx, q in enumerate(form.elements):
            # put the scores back into the database and go to thank you page...
            votes_elements[idx].score = q.rating.data
            db.session.add(votes_elements[idx])

        # and persist to database
        db.session.commit()
        
        # set voted flag
        if form.submit.data:
            current_user.has_voted = True
            db.session.add(current_user)
            db.session.commit()
            return redirect(url_for('main.success'))
        else:
            current_user.has_saved = True
            db.session.add(current_user)
            db.session.commit()
            flash("Je voorkeuren zijn opgeslagen, druk op stemmen om je stem te registeren")

    return render_template('poll.html',
        secret_key=current_user.secret_key, 
        titles_functions=titles_functions,
        titles_elements=titles_elements,    
        form=form)


@main.route('/success')
@login_required
def success():
    logout_user()
    return render_template('success.html')
