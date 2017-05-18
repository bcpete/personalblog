from google.appengine.ext import db

class User(db.Model):
    username = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)

class Post(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)

class Comment(db.Model):
    author = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
