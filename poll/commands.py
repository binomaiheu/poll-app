import click
from flask.cli import with_appcontext

from sqlalchemy import func, desc

from .models import db, User, Vote, Option
from .tools import get_vote_status, key_gen

@click.command('createdb')
@click.argument("num_users")
@with_appcontext
def create_db(num_users):
    """
    Command to initilize the database with the amount of users given
    """
    db.drop_all()
    db.create_all()

    # Confugration
    option_list = {
        "Functies": [
            "Ontmoetingsplaats voor jong en oud",
            "Groenzone, nadruk op bomen, struiken, vegetatie",
            "Sportterrein",
            "Zone om activiteiten te organiseren met de wijk",
            "Speeltuin / avontuurlijke zone voor de kinderen"
        ],
        "Elementen": [
            "Trampoline / springkussen ingewerkt in de grond",
            "Petanquebaan",
            "Bomen",
            "Fruitbomen",
            "Notenbomen",
            "Voetbal pleintje met doeltjes",
            "Fietsdraaimolen",
            "Deadride zoals achter gemeentehuis in Destelbergen",
            "Basketbal goal",
            "Grillplaats",
            "Heuveltje als speels landschapselement",
            "Tennis terrein",
            "Padel terrein",
            "Schommels",
            "Wipplank",
            "Zandbak",
            "Blote voetenpad",
            "Waterfietsen voor op de vijver :)",
            "Pluktuin met bessenstruken, rabarber, e.d.",
            "Bloemenweide voor de bijtjes",
            "Zwemvijver",
            "Electriciteit en watervoorziening om activiteiten te kunnen organiseren",
            "Workout toestellen voor adolescenten en volwassenen",
            "Schommelbank voor ouderen of mindervaliden",
            "Hangmatten",
            "Zitbanken",
            "Picnic tafels",
            "Levensgroot schaakspel",
            "Lage boomhut",
            "Atletiek oefenplein zoals vb. Kogelstoten, speerwerpen",
            "Open stuk met enkel gras voor activiteiten"
        ]
    }
    # different options
    functions = [ 
        Option(description=option_list["Functies"][i], category="Functies") 
        for i in range(len(option_list["Functies"])) 
    ]
    elements = [ 
        Option(description=option_list["Elementen"][i], category="Elementen") 
        for i in range(len(option_list["Elementen"])) 
    ]

    # generate list of num_users users with random secret key
    num_users = int(num_users)
    users = [ User(secret_key=key_gen(), weight=1.) for i in range(num_users) ]

    # insert in the database
    db.create_all()
    db.session.bulk_save_objects(functions)
    db.session.bulk_save_objects(elements)
    db.session.bulk_save_objects(users)

    db.session.commit()

    # now generate the votes
    # query the whole list to get the id's from the database & reset the score for all 
    users = User.query.all()
    options = Option.query.all()
    for u in users:
        for q in options:
            v = Vote(user_id=u.id, option_id=q.id, score=0)
            db.session.add(v)
    db.session.commit()


@click.command('dropdb')
@with_appcontext
def drop_db():
    """
    Resets the database
    """
    db.drop_all()


@click.command('adduser')
@with_appcontext
def add_user():
    """
    Adds a user to the user table & initialises the votes for him/her. 
    """

    # Need to import those here and not at the top otherwise we get circular import errors
    user = User(secret_key=key_gen(), weight=1.)
    print(f"Adding user, key={user.secret_key}")

    db.session.add(user)

    for q in Option.query.all():
        v = Vote(user_id=user.id, option_id=q.id, score=0)
        db.session.add(v)
    
    db.session.commit()


@click.command('pollstats')
@with_appcontext
def poll_stats():
    """
    Prints the current status of the poll
    """
    print('Users')
    print('-----')
    for u in User.query.all():
        print(f"  User={u.secret_key}, has_voted={u.has_voted}, has_saved={u.has_saved}")

    print('Poll statistics')
    print('---------------')
    stat = get_vote_status()
    print(f"  Users voted : {stat['n_votes']}/{stat['n_users']}")
    
    print('Function votes')
    print('--------------')
    results = db.session.query(Option, Vote, func.sum(Vote.score).label("total_score"))\
                .join(Option, Vote.option_id == Option.id)\
                .filter(Option.category == "Functies")\
                .group_by(Vote.option_id)\
                .order_by(desc("total_score"))
    for idx, r in enumerate(results):
        print(  f"  [{idx+1}] {r[0].description} (total score={r[2]})")

    print('Elements votes')
    print('--------------')
    results = db.session.query(Option, Vote, func.sum(Vote.score).label("total_score"))\
                .join(Option, Vote.option_id == Option.id)\
                .filter(Option.category == "Elementen")\
                .group_by(Vote.option_id)\
                .order_by(desc("total_score"))
    for idx, r in enumerate(results):
        print(  f"  [{idx+1}] {r[0].description} (total score={r[2]})")