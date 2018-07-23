import webapp2
import json
import datetime

from google.appengine.api import memcache
from google.appengine.api import users


class GetLoginUrlHandler(webapp2.RequestHandler):
    def dispatch(self):
        result = {
        'url' : users.create_login_url('/')
        }
        send_json(self, result)


def send_json(request_handler, props):
    request_handler.response.content_type = 'application/json'
    request_handler.response.out.write(json.dumps(props))


class GetUserHandler(webapp2.RequestHandler):
    def dispatch(self):
        email = get_current_user_email()
        result = {}
        if email:
            result['user'] = email
        else:
            result['error'] = 'User is not logged in.'
        send_json(self, result)


def get_current_user_email():
    current_user = users.get_current_user()
    if current_user:
        return current_user.email()
    else:
        return None


class GetLogoutUrlHandler(webapp2.RequestHandler):
    def dispatch(self):
        result = {
        'url' : users.create_logout_url('/logout')
        }
        send_json(self, result)
        
        
class LogDataHandler(webapp2.RequestHandler):
    def dispatch(self):
        data = {}
        
        
class ViewReportHandler(webapp2.RequestHandler):
    
    
class ViewHistoryHandler(webapp2.RequestHandler):
    
    
app = webapp2.WSGIApplication([
    ('/', GetUserHandler),
    ('/user', GetUserHandler),
    ('/login', GetLoginUrlHandler),
    ('/logout', GetLogoutUrlHandler),
    ('/data', LogDataHandler),
    ('/report', ViewReportHandler),
    ('/history', ViewHistoryHandler),
],   debug=True)
