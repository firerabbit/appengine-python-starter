from datetime import tzinfo, timedelta, datetime

import logging

import pytz
from pytz import timezone
from pytz import gae

TIMEZONES = [
  ('Pacific/Midway', '(GMT-11:00) Midway, Samoa'),
  ('US/Hawaii', '(GMT-10:00) Hawaii'),
  ('US/Alaska', '(GMT-9:00) Alaska'),
  ('US/Pacific', '(GMT-8:00) US Pacific'),
  ('US/Mountain', '(GMT-7:00) US Mountain'),
  ('US/Central', '(GMT-6:00) US Central'),
  ('US/Eastern', '(GMT-5:00) US Eastern'),
  ('America/Caracas', '(GMT-4:30) Venezuela'),
  ('America/Halifax', '(GMT-4:00) Atlantic'),
  ('America/St_Johns', '(GMT-3:30) Newfoundland'),
  ('America/Argentina/Buenos_Aires', '(GMT-3:00) Brazil, Argentina'),
  ('Atlantic/South_Georgia', '(GMT-2:00) Mid-Atlantic'),
  ('Atlantic/Azores', '(GMT-1:00 hour) Azores'),
  ('GMT', '(GMT) Western Europe'),
  ('Europe/Paris', '(GMT+1:00) Central Europe'),
  ('Africa/Johannesburg', '(GMT+2:00) South Africa'),
  ('Europe/Moscow', '(GMT+3:00) Baghdad, Moscow'),
  ('Asia/Tehran', '(GMT+3:30) Iran'),
  ('Asia/Dubai', '(GMT+4:00) Gulf'),
  ('Asia/Kabul', '(GMT+4:30) Afghanistan'),
  ('Asia/Karachi', '(GMT+5:00) Pakistan'),
  ('Asia/Kolkata', '(GMT+5:30) India'),
  ('Asia/Kathmandu', '(GMT+5:45) Nepal'),
  ('Asia/Dhaka', '(GMT+6:00) Bangladesh'),
  ('Asia/Jakarta', '(GMT+7:00) Bangkok, Jakarta'),
  ('Asia/Taipei', '(GMT+8:00) China'),
  ('Asia/Tokyo', '(GMT+9:00) Japan, Korea'),
  ('Australia/Darwin', '(GMT+9:30) Central Australia'),
  ('Australia/Sydney', '(GMT+10:00) Eastern Australia'),
  ('Pacific/Noumea', '(GMT+11:00) New Caledonia'),
  ('Pacific/Auckland', '(GMT+12:00) New Zealand'),
]


def is_valid_timezone(tz_name):
  return tz_name in pytz.all_timezones


def local_to_utc(dt):
  """ Converts TZ-aware datetime object to UTC.
  """
  if dt.tzinfo is None:
    naive_to_utc(dt)
  return pytz.utc.normalize(dt.astimezone(pytz.utc))


def naive_to_local(dt, tz_name):
  """ Converts naive (w/o tzinfo) datetime object to specified local timezone.
      tz_name = name of timezone, ex: 'US/Pacific'.
  """
  tz = pytz.timezone(tz_name)
  return tz.normalize(tz.localize(dt))


def naive_to_utc(dt):
  """ Converts naive datetime object to UTC.
  """
  return naive_to_local(dt, 'UTC').astimezone(pytz.utc)


def utc_to_local(dt, tz_name):
  """ Converts TZ-aware UTC datetime to local timezone.
      tz_name = name of timezone, ex: 'US/Pacific'.
  """
  if dt.tzinfo is None:
    dt = dt.replace(tzinfo=pytz.utc)  # naive datetime, assume it's UTC
  assert dt.tzinfo is pytz.utc
  tz = pytz.timezone(tz_name)
  return dt.astimezone(tz)


def now_as_local(tz_name):
  return naive_to_local(datetime.now(), tz_name)


def now_as_utc():
  return naive_to_utc(datetime.now())
