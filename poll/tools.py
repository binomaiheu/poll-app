import string
import random
import pandas as pd

from sqlalchemy import func, desc

from poll import db
from poll.models import Option, Vote, User

def key_gen(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_list_of_elements():
    return Option.query.filter_by(category="Elementen").order_by(Option.id).all()

def get_list_of_functions():
    return Option.query.filter_by(category="Functies").order_by(Option.id).all()

def get_user_scores(secret_key: str):
    """
    Returns the scores from the db for the given secret key
    """
    return db.session.query(Option, Vote).\
            join(Vote, Vote.option_id == Option.id).\
            join(User, Vote.user_id == User.id).\
            filter(User.secret_key == secret_key).\
            order_by(Option.id).all()

def get_vote_status():
    """
    Returns the vote status, returns list
    [ #votes, total ]
    """
    return {
        "n_votes": db.session.query(func.count(User.id)).filter(User.has_voted).one()[0],
        "n_users": db.session.query(func.count(User.id)).one()[0]
    }


def get_results():
    """
    Returns a dataframe with the results
    """    
    df = pd.DataFrame()
    results = db.session.query(Option, func.sum(Vote.score).label("total_score"))\
                .join(Option, Vote.option_id == Option.id)\
                .filter(Option.category == "Functies")\
                .group_by(Option.id)\
                .order_by(desc("total_score"))
    for idx, r in enumerate(results):
        df = df.append({"type": "function", "description": r[0].description, "score": r[1]}, ignore_index=True)
            
    results = db.session.query(Option, func.sum(Vote.score).label("total_score"))\
                .join(Option, Vote.option_id == Option.id)\
                .filter(Option.category == "Elementen")\
                .group_by(Option.id)\
                .order_by(desc("total_score"))
    for idx, r in enumerate(results):
        df = df.append({"type": "elements", "description": r[0].description, "score": r[1]}, ignore_index=True)

    return df