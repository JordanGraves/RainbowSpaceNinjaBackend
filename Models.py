from google.appengine.ext import db


class Score(db.Model):
    name = db.StringProperty(required=True)
    score = db.FloatProperty(required=True)
