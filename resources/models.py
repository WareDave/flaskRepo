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
    name = CharField()
    breed = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    owner = ForeignKeyField(User, backref = 'characters')

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Character], safe=True)
    print('TABLES Bitches')
    DATABASE.close()