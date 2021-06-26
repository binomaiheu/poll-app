from poll import db, app
from poll.models import *

from poll.tools import key_gen


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
        "Bomen, fruitbomen, notenbomen",
        "Bessenstruiken",
        "Voetbal pleintje met doeltjes",
        "Fietsdraaimolen",
        "Deadride zoals achter gemeentehuis in Destelbergen",
        "Basketbal goal",
        "Grillplaats",
        "Heuveltje als speels landschapselement",
        "Tennis / padel terrein",
        "Schommels",
        "Houten wipplank",
        "Zandbak",
        "Blote voetenpad",
        "Wipplank",
        "Pluktuin met bessenstruken, rabarber, ...",
        "Bloemenweide voor de bijtjes",
        "Zwemvijver",
        "Electriciteit en watervoorziening om activiteiten te kunnen organiseren",
        "Workout toestellen voor adolescenten en volwassenen",
        "Schommelbank voor ouderen of mindervaliden, vb om rolwagen op te rijden, vastzetten en dan schommelen",
        "Hangmatten",
        "Zitbanken",
        "Picnic tafels",
        "Levensgroot schaakspel",
        "Lage boomhut",
        "Atletiek oefenplein zoals vb. Kogelstoten, speerwerpen",
        "Open stuk met enkel gras voor activiteiten"
    ]
}

num_users = 10



# different options
functions = [ Option(description=option_list["Functies"][i], category="Functies") for i in range(len(option_list["Functies"])) ]
elements = [ Option(description=option_list["Elementen"][i], category="Elementen") for i in range(len(option_list["Elementen"])) ]


# generate list of num_users users with random secret key
users = [ User(secret_key=key_gen(), weight=1.) for i in range(num_users) ]

# insert in the database
db.app = app
db.init_app(app)
db.create_all()
db.session.bulk_save_objects(functions)
db.session.bulk_save_objects(elements)
db.session.bulk_save_objects(users)

db.session.commit()