import datetime

from mongoengine import *

from user.models import User

connect('R2D2')


class Sentence(Document):
    text = StringField(max_length=4096, null=False)
    # TODO refactor
    polarityAvg = FloatField(default=0, null=False)


class SentenceHistory(Document):
    sentenceId = ReferenceField(Sentence, reverse_delete_rule=CASCADE, null=False)
    userId = ReferenceField(User, reverse_delete_rule=CASCADE)
    polarity = IntField(null=False)
    ip = StringField(max_length=120)
    date = DateTimeField(default=datetime.datetime.now)
