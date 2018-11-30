"""
download the google appengine sdk:
https://storage.googleapis.com/appengine-sdks/featured/GoogleAppEngineLauncher-1.9.80.dmg

create a new project:
admin console: http://localhost:8000
web server: http://localhost:8085
interactive console: http://localhost:8000/console

create a user from the console:
from model import UserProfile
u = UserProfile.create('foo@bar.com', 'test-password')
print u.json()

"""

# Python imports
import constants
import logging
import os
import webapp2
from webapp2_extras import sessions

from django import template
from django.template import Context, Template
from django.template.loader import get_template

import handlers
from utils import time_util

urls = [
  ('/', handlers.MainHandler),
  ('/_ah/warmup', handlers.Warmup),
  ('/snake', handlers.SnakeHandler),
  ('/signup', handlers.SignupHandler),
  ('/login', handlers.LoginHandler),
  ('/user', handlers.UserHandler),
]

template.add_to_builtins('django.contrib.humanize.templatetags.humanize')
template.add_to_builtins('filters.filters')

app = webapp2.WSGIApplication(urls, config=constants.APP_CONFIG)
