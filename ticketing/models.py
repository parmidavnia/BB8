import datetime

from django.db import models
from mongoengine import *

from user.models import User
connect('R2D2')

#class Ticket(models.Model):
class Ticket(Document):
    text = StringField(max_length=4096, null=False)
    # TODO refactor
    userId = ReferenceField(User, reverse_delete_rule=CASCADE)
