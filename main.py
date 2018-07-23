import webapp2
import json
import datetime
import logging
import jinja2

from google.appengine.ext import ndb
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

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

def get_current_user_distance():
    current_distance = users.get_current_distance()
    if current_distance:
        return current_user.distance()
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
	def post(self):
		mpg = float(self.request.get('mpg'))
		distance = float(self.request.get('distance'))
		transportation = self.request.get('way')
		comment = self.request.get('comment')
		co2_per_mile = 20.00 / mpg
#		logs data to admin page even when deployed
		logging.info(co2_per_mile)
#		transportation and comment are both Unicode strings, unicode strings and str can be compared and return true
#		if transportation == 'bike':
#			print('true')
		print(co2_per_mile, distance, transportation, comment)
class ViewHistoryHandler(webapp2.RequestHandler):
	def dispatch(self):
        result = {
            'url' : users.create_logout_url('/logout')
        }
        send_json(self, result)


class Log(ndb.Model):
    email = ndb.StringProperty(required=True)
    distance = ndb.FloatProperty(required=True)
    timestamp = ndb.StringProperty(required=True)

    def __init__(self, email, distance):
             self.email = email
             self.distance = distance
             self.timestamp = datetime.datetime.now()
    def to_dict(self):
            log = {
                'user': self.email,
                'distance': self.distance,
                'timestamp': self.timestamp.strftime('%Y-%m-%d %I:%M:%S')
            }
            return log

class LogDataHandler(webapp2.RequestHandler):
    def post(self):
        email = get_current_user_email()
        distance = self.request.get('distance')
        print distance
#        if email:
#            log = Log(email=email, distance=distance, timestamp=str(datetime.datetime.now()))
#        if email:
#            result['data'] = []
#            messages = ndb.get('data')
#            for message in messages:
#                log['data'].append(data.to_dict())
#        else:
#            log['error'] = 'User is not logged in.'
#        log.put()

class ViewHistoryHandler():
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
