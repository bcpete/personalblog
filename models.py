from google.appengine.ext import db

class User(db.Model):
    username = db.StringProperty(required = True)
    pw_hash  = db.StringProperty(required = True)

class Post(db.Model):
    title  = db.StringProperty(required = True)
    body   = db.TextProperty(required = True)
    author = db.ReferenceProperty(User, required = True)

class Comment(db.Model):
    author = db.StringProperty(required = True)
    body   = db.TextProperty(required = True)

class Category(db.Model):
    post = db.ReferenceProperty(Post,
                                collection_name = 'posts')
    category_name = db.StringProperty(
            choices=('Thoughts', 'Tech', 'Reading, Watching, Listening to', "One Player"))
