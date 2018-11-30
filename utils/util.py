
import re
import logging
import hashlib
import urllib


def get_hash(s):
  return str(hashlib.md5(s).hexdigest())


def get_user_agent(request):
  return request.headers.get('User-Agent') or ''


def is_iphone(user_agent):
  return str(user_agent).lower().find("iphone") >= 0


def is_ipad(user_agent):
  return str(user_agent).lower().find("ipad") >= 0


def is_android(user_agent):
  return str(user_agent).lower().find("android") >= 0


def is_mobile(request):
  agent = get_user_agent(request)
  return is_iphone(agent) or is_android(agent)
