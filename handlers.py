
# Python imports
import constants
import datetime
import logging
import os
import re
import random
import json
import sys
import time
import urllib
import quopri
import webapp2
from webapp2_extras import sessions

from django import template
from django.template import Context, Template
from django.template.loader import get_template

# AppEngine imports.
from google.appengine.api import datastore
from google.appengine.api import images
from google.appengine.api import mail
from google.appengine.api import memcache
from google.appengine.api import taskqueue
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import util as gutil
from google.appengine.ext.db import Key

# local imports
from model import UserProfile
from utils import util
import wrappers


def get_recent_users(num=10):
  """ Return the 10 most recent users """
  return UserProfile.all().order('-date_created').fetch(num)


class Handler(webapp.RequestHandler):
  """ Common base handler for all our handlers """

  @webapp2.cached_property
  def session(self):
    return self.session_store.get_session(backend='datastore')

  @webapp2.cached_property
  def user(self):
    user_id = int(self.session.get('user_id') or 0)
    if user_id:
      return UserProfile.get_by_id(user_id)

  def logout(self):
    self.session.pop('user_id', None)

  def redirect(self, url, message=None):
    """ Wrap the built in redirect function to pass a message via session """
    if message:
      self.session['message'] = message
    super(Handler, self).redirect(str(url))

  def unauthorized(self):
    # TODO: Type a better exception
    raise Exception('unauthorized')

  def handle_exception(self, e, debug=None):
    logging.error("Exception: %s", e)
    if e and e.message == 'unauthorized':
      return self.redirect('/login', 'login required')
    self.render('error.html', {'exception': e})

  def get_last_message(self):
    return self.session.pop('message', '')

  def render(self, template_name, d=None):
    d = d or {}
    agent = util.get_user_agent(self.request)
    iphone = util.is_iphone(agent)
    ipad = util.is_ipad(agent)
    android = util.is_android(agent)

    d.update({
      'message': self.get_last_message(),
      'user': getattr(self, 'user', None),
      'mobile': iphone or android,
      'touch': iphone or ipad or android,
      'iphone': iphone,
      'ipad': ipad,
    })

    self.response.out.write(self.render_to_string(template_name, d))

  def render_to_string(self, template_name, d=None):
    d = d or {}
    t = get_template(template_name)
    return t.render(Context(d))

  def json(self, data):
    json = json.dumps(data)
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json)

  def dispatch(self):
    """ Magic to hookup a session to webapp2 """
    self.session_store = sessions.get_store(request=self.request)
    try:
      webapp2.RequestHandler.dispatch(self)
    except Exception, err:
      self.handle_exception(err)
    finally:
      self.session_store.save_sessions(self.response)


class MainHandler(Handler):

  def get(self):
    data = {
      'welcome_message': 'Welcome to the sample app!',
      'users': get_recent_users(),
    }
    self.render('index.html', data)


class SnakeHandler(Handler):

  def get(self):
    logging.info("Cron running every 2 hours")
    # TODO: Do some snaking here.


class SignupHandler(Handler):

  def post(self):
    email = self.session['email'] = self.request.get('email', '').lower()
    password = self.request.get('password')

    # Nothing to log in with
    if not email or not password:
      return self.redirect('/signup', 'email and password required')

    # Password matches the user we found with this email
    user = UserProfile.get_by_email(email)
    if user:
      return self.redirect('/signup', 'user already exists')

    user = UserProfile.create(email, password)
    self.session['user_id'] = user.id

    # Failed to login
    self.redirect('/')

  def get(self):
    data = {
      'email': self.session.get('email'),
    }
    self.render('signup.html', data)

class LoginHandler(Handler):

  def post(self):
    email = self.session['email'] = self.request.get('email', '').lower()
    password = self.request.get('password')

    if self.user:
      return self.redirect('/user', 'already logged in')

    # Nothing to log in with
    if not email or not password:
      return self.redirect('/login', 'missing password')

    # Password matches the user we found with this email
    user = UserProfile.get_by_email(email)
    if user and user.check_password(password):
      self.session['user_id'] = user.id
      return self.redirect('/')

    # Failed to login
    self.redirect('/login', 'user not found')

  def get(self):
    # If we got to the /login page, log the user out
    self.logout()

    data = {
      'email': self.session.get('email'),
    }
    self.render('login.html', data)


class UserHandler(Handler):

  @wrappers.user_required
  def get(self):
    data = {
      'foo': 'bar',
    }
    self.render('user.html', data)


class Warmup(Handler):
  """ Warmup request """
  def get(self):
    logging.info(os.environ)

