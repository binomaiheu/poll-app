import string
import random

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
    
    return db.session.query(Option, Vote, User).\
            outerjoin(Vote, Vote.option_id == Option.id).\
            outerjoin(User, Vote.user_id == User.id).\
            filter(User.secret_key == secret_key).all()
