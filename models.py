import datetime
from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('test1.sqlite')
# DATABASE = PostgresqlDatabase('saves_the_day_app')

class User(UserMixin, Model):
    username = CharField()
    email = CharField(unique = True)
    created_at = DateTimeField(default=datetime.datetime.now)
    password = CharField()

    class Meta:
        database = DATABASE

class Character(Model):
    name = CharField(unique = True)
    created_at = DateTimeField(default=datetime.datetime.now)
    loggedUser_id = ForeignKeyField(User, backref = 'characters')
    classLevel = CharField(null = False)
    background = CharField(null = False)
    race = CharField(null = False)
    alignment = CharField(null = False)
    exp = CharField(null = False)
    strength = CharField(null = False)
    dex = CharField(null = False)
    const = CharField(null = False)
    intelligence = CharField(null = False)
    wisdom = CharField(null = False)
    charisma = CharField(null = False)
    inspiration = CharField(null = False)
    saving = CharField(null = False)
    skills = CharField(null = False)
    passive = CharField(null = False)
    armorclass = CharField(null = False)
    init = CharField(null = False)
    speed = CharField(null = False)
    currenthp = CharField(null = False)
    temphp = CharField(null = False)
    hdice = CharField(null = False)
    dsaves = CharField(null = False)
    atks_spells = CharField(null = False)
    equipment = CharField(null = False)
    fandt = CharField(null = False) 
   
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Character], safe=True)
    print('TABLES Bitches')
    DATABASE.close() 