#/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, jinja2, os, re
from google.appengine.ext import db
from models import Post, User, Comment
import hashutils

template_dir = (os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
        autoescape = True)

class Handler(webapp2.RequestHandler):
    """Helper class with all the useful methods that my request handlers will need"""

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t=jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def login_user(self, user):
        """Login a user"""
        user_id = user.key().id()
        self.set_secure_cookie('user_id', str(user_id))

    def logout_user(self):
        """Logout A user"""
        self.set_secure_cookie('user_id', '')

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        if cookie_val:
            return hashutils.check_secure_val(cookie_val)

    def set_secure_cookie(self, name, val):
        cookie_val = hashutils.make_secure_val(val)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, cookie_val))

    def initialize(self, *a, **kw):
        """
        Filter to restrict acces to certain pages when not logged in. if the request path is
        in the global auth_paths list, then the user must be signed in to access the path/resource.
        """
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.get_by_id(int(uid))

        if not self.user and self.request.path in auth_paths:
            self.redirect('/')

"""
Handlers for the front page, and "/" that redirects to "/home"
"""

class MainHandler(Handler):
    def get(self):
        self.redirect('/home')

class FrontpageHandler(Handler):
    def get(self):
        self.render('frontpage.html')

"""
Handler for making a new post, get method displays the form, and post method checks if the post is valid.
if the post is valid, the method creates a new Post object and stores it in the database. Redirects to /{Category_name}/{post_id}
"""
class NewPostHandler(Handler):
    def get(self, title = "", body = "", category = "", error = "")
        self.render('newpost.html', title=title, body=body, category=category, error=error)

    def post(self):
        title         = self.request.get("title")
        body          = self.request.get("body")
        category      = self.request.get("category")

    if title and body:
        post = Post(
                title  = title,
                body   = body,
                author = self.user)
        category = Category(
                category_name = category,
                post = post)
        post.put()
        category.put()

        PostId = post.key().id()


        self.redirect("/{}/{}".format(category, PostId))

    else:
        error = "You forgot a title, body, or a category bozo."
        self.render(title, body, category, error)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/home', FrontpageHandler),
], debug=True)

""" List of paths that user must be logged in to access"""
auth_paths = [
        '/login',
        '/newpost'
]
