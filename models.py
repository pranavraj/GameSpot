from datetime import datetime
import random
from mongoengine.queryset.manager import queryset_manager
from app import db

class User(db.DynamicDocument):
    email = db.StringField(required=True)
    name = db.StringField(max_length=50)
    type = db.StringField(max_length=50)

    def __str__(self):
        return "{} ({})".format(name, type)

    def save_if_not_present(self):
        self.save()


class Game(db.Document):
    name = db.StringField(max_length=64, required=True)
    description = db.StringField()
    link = db.StringField(required=True)

    def __str__(self):
        return self.name

class League(db.Document):
    title = db.StringField(max_length=120, required=True)
    author = db.ReferenceField(User, reverse_delete_rule=db.CASCADE)
    game = db.ReferenceField(Game, reverse_delete_rule=db.NULLIFY)
    users = db.ListField(db.ReferenceField(User, reverse_delete_rule=db.PULL))
    created_at = db.DateTimeField(default=datetime.utcnow)
    starting_at = db.DateTimeField(default=datetime.utcnow)
    ending_at = db.DateTimeField(default=datetime.utcnow)
 
    @queryset_manager
    def live_posts(cls, queryset):
        return queryset.filter(published=True)

    def __str__(self):
        return self.title
