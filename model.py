
from google.appengine.ext import blobstore
from google.appengine.ext import db

from utils import util


class BaseModel(db.Model):
  """ Common base model so we can write some nice helper functions """
  # These 2 properties are always good to have on a new model
  date_created = db.DateTimeProperty(auto_now_add=True)
  date_modified = db.DateTimeProperty(auto_now=True)

  def __str__(self):
    """ Print something useful for this entity """
    if self.is_saved():
      return '%s:%s' % (self.key().kind(), self.key().id_or_name())
    return '%s:unsaved' % self.__class__.__name__

  @property
  def id(self):
    """ Quick helper for getting an entity id """
    return self.key().id_or_name()

  def equals(self, other_or_key):
    """ Return true if the keys are equal """
    key = gae_tools.key_or_entity(other_or_key)
    return str(self.key()) == str(key)

  def refresh(self):
    """ Refetches an entity from the datastore if entity may be stale. """
    return db.get(self.key())

  def json_date(cls, date):
    if not date:
      return None
    seconds = int(time.mktime(date.timetuple()))
    return seconds * 1000 + (date.microsecond / 1000)


class UserProfile(BaseModel):

  name = db.StringProperty(default=None)
  email = db.EmailProperty(required=True)
  password = db.StringProperty(required=True)
  image = blobstore.BlobReferenceProperty(indexed=False, required=False)

  @classmethod
  def get_by_email(cls, email):
    if not email:
      return
    return cls.all().filter('email =', email.lower().strip()).get()

  @classmethod
  def create(cls, email, password):
    assert email and password
    email = email.lower().strip()
    assert email
    existing_user = cls.get_by_email(email)
    assert not existing_user
    e = cls(email=email, password=util.get_hash(password))
    e.put()
    return e

  def check_password(self, password):
    """ Check to see if a password matches what we've got stored """
    assert self.password and password
    return self.password == util.get_hash(password)

  def json(self):
    return {
      'user_id': self.id,
      'name': self.name,
      'email': self.email,
      'has_password': bool(self.password),
      'date': self.json_date(self.date),
    }
