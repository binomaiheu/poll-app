from enum import unique
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), 
        onupdate=db.func.current_timestamp())
    

class User(Base):

    __table_name__ = "user"

    secret_key = db.Column(db.String(10), unique=True) # secret key used for authenticating whether you are allowed to vote
    weight = db.Column(db.Float, default=1.) 

    votes = db.relationship("Vote", backref="user")


class Option(Base):

    __table_name__ = "option"

    category = db.Column(db.String(40)) # a category for the option
    description = db.Column(db.String(500))  # name for the question

    votes = db.relationship("Vote", backref="option")

    def __repr__(self):
        return self.description


class Vote(Base):

    __table_name__ = "vote"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    option_id = db.Column(db.Integer, db.ForeignKey("option.id"))
    score = db.Column(db.Integer, default=0) # the score the user assigned to the option

    # add uniqu constraint : one user, one option, one vote !!
    __table_args__ = (
        db.UniqueConstraint("user_id", "option_id"),
    )

    def __repr__(self):
        return f"score={self.score}"