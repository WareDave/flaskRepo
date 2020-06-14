import datetime
from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('test2.sqlite')
# DATABASE = PostgresqlDatabase('saves_the_day_app')

class User(UserMixin, Model):
    username = CharField()
    email = CharField(unique = True)
    created_at = DateTimeField(default=datetime.datetime.now)
    password = CharField()

    class Meta:
        database = DATABASE
        
        class Legal(Model):
    name = CharField(unique = True)
    created_at = DateTimeField(default=datetime.datetime.now)
    loggedUser = ForeignKeyField(User, backref = 'legals')
    par1 = CharField()
    par2 = CharField()
    par3 = CharField() 
    ia1 = IntegerField()
    ia2 = IntegerField()
    ia3 = IntegerField()
    
   
    class Meta:
        database = DATABASE
        
class Stock(model):
    created_at = DateTimeField(default=datetime.datetime.now)
    loggedUser = ForeignKeyField(User, backref = 'legals')
    category = CharField()
    brend = CharField()
    description = CharField()
    size = CharField()
    price = CharField()
    fee = CharField()
    split = CharField()
    coder =CharField()
    venderID = CharField()

    class Meta:
        database = DATABASE

class Character(Model):
    name = CharField(unique = True)
    created_at = DateTimeField(default=datetime.datetime.now)
    loggedUser = ForeignKeyField(User, backref = 'characters')
    classLevel = CharField()
    background = CharField()
    race = CharField()
    # alignment = CharField()
    # experience = IntegerField()
    strength = IntegerField()
    dex = IntegerField()
    const = IntegerField()
    intelligence = IntegerField()
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
    atks_spells = TextField()
    equipment = TextField()
    fandt = TextField() 
   
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Character], safe=True)
    print('TABLES Bitches')
    DATABASE.close() 