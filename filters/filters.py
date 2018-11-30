
import pretty

from django import template

register = template.Library()

from utils import time_util


@register.filter
def pretty_date(value, short=None):
  if short:
    return pretty.date(value, False, True, False)
  else:
    return pretty.date(value)


@register.filter
def tz(value, arg=None):
  if value:
    timezone = 'US/Pacific'
    if arg and arg.timezone:
      timezone = arg.timezone
    return time_util.utc_to_local(value, timezone)
  else:
    return None


@register.filter
def truncate(value, arg):
    """
    Truncates a string after a given number of chars
    Argument: Number of chars to truncate after
    """
    try:
        length = int(arg)
    except ValueError: # invalid literal for int()
        return value # Fail silently.
    if not isinstance(value, basestring):
        value = str(value)
    if (len(value) > length):
        return value[:length] + "..."
    else:
        return value
