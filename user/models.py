import datetime

from mongoengine import *

connect('R2D2')


class User(Document):
    firstName = StringField(max_length=120, null=False)
    lastName = StringField(max_length=360, null=False)
    email = EmailField(max_length=360, unique=True)
    password = StringField(max_length=120, null=False)
    bio = StringField(max_length=1024)
    token = StringField(max_length=4096, unique=True)
    role = StringField(max_length=32, default='TAGGER')
    registrationDate = DateTimeField(default=datetime.datetime.now)
    score = IntField(default=0)
