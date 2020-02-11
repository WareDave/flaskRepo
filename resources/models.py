import datetime
from peewee import *
from flask_login import UserMixin

# DATABASE = SqliteDatabase('charactertest.sqlite')
DATABASE = PostgresqlDatabase('D&D_app')

class User(UserMixin, Model):
    username = CharField(unique = True)
    email = CharField(unique = True)
    password = CharField()

    class Meta:
        database = DATABASE

class Character(Model):
    name = CharField(unique = True)
    realm = CharField()
    classLevel = CharField()
    background = CharField()
    race = CharField()
    alighment = CharField()
    exp = CharField()
    strength = CharField()
    dex = CharField()
    const = CharField()
    intelligence = CharField()
    wisdom = CharField()
    charisma = CharField()
    inspiration = CharField()
    saving = CharField()
    skills = CharField()
    passive = CharField()
    armorclass = CharField()
    init = CharField()
    speed = CharField()
    currenthp = CharField()
    temphp = CharField()
    hdice = CharField()
    dsaves = CharField()
    atks_spells = CharField()
    equipment = CharField()
    fandt = CharField() 
    created_at = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(User, backref = 'characters')

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Character], safe=True)
    print('TABLES Bitches')
    DATABASE.close()