import webapp2
import json
import datetime

from google.appengine.api import ndb
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
        print(Log.query().fetch())
        


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
        
        
class Log(ndb.Model):
    email = ndb.StringProperty(required=True)
    distance = ndb.FloatProperty(required=True)
    timestamp = ndb.StringProperty(required=True)
    
#     def __init__(self, email, distance):
#             self.email = email
#             self.distance = distance
#             self.timestamp = datetime.datetime.now()
    def to_dict(self):
            log = {
                'user': self.email,
                'distance': self.distance,
                'timestamp': self.timestamp.strftime('%Y-%m-%d %I:%M:%S')
            }
            return log
        
class LogDataHandler(webapp2.RequestHandler):
        def dispatch(self):
            email = get_current_user_email()
            if email:
                log = Log(email=email, distance=10, timestamp=str(datetime.datetime.now()))
                if email:
                    result['data'] = []
                    messages = ndb.get('data')
                    for message in messages:
                        log['data'].append(data.to_dict())
                else:
                    log['error'] = 'User is not logged in.'
                log.put()

class ViewReportHandler(webapp2.RequestHandler):
    pass
class ViewHistoryHandler(webapp2.RequestHandler):
    pass
    
app = webapp2.WSGIApplication([
    ('/', GetUserHandler),
    ('/user', GetUserHandler),
    ('/login', GetLoginUrlHandler),
    ('/logout', GetLogoutUrlHandler),
    ('/data', LogDataHandler),
    ('/report', ViewReportHandler),
    ('/history', ViewHistoryHandler),
],   debug=True)
