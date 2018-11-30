
APP_CONFIG = {}
APP_CONFIG['webapp2_extras.sessions'] = {
  'secret_key': 'my-app-secret',
  'cookie_name': 'session',
  'cookie_args': { 'max_age':60*60*24*30*12*10 },
}
