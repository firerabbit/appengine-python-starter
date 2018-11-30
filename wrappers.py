
# Usage: @wrappers.user_required
def user_required(method):
  def wrapper(self, *args, **kwargs):
    if not self.user:
      return self.unauthorized()
    return method(self, *args, **kwargs)

  return wrapper
