import webapp2
import json
import datetime
import logging
import jinja2
import os

from google.appengine.ext import ndb
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class GetLoginUrlHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.redirect(users.create_login_url('/'))
#        result = {
#        'url' : users.create_login_url('/')
#        }
#        send_json(self, result)

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


class GetHomePageHandler(webapp2.RequestHandler):
    def get(self):
        email = get_current_user_email()
        print 'this renders the jinja template'
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(email=email))


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

def get_current_user_transportation():
    current_transportation = users.get_current_transportation()
    if current_transportation:
        return current_user.transportation()
    else:
        return None


class GetLogoutUrlHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.redirect(users.create_logout_url('/'))
#        result = {
#        'url' : users.create_logout_url('/logout')
#        }
#        send_json(self, result)


class LogDataHandler(webapp2.RequestHandler):
    def post(self):
        email = get_current_user_email()
        print email
        if email:
            mpg = float(self.request.get('mpg'))
            distance = float(self.request.get('distance'))
            transportation = self.request.get('way')
            comment = self.request.get('comment')
            co2 = 20.00 / mpg * distance
            if transportation == "runing":
                calories = distance * 100
            elif transportation == "walking":
                calories = distance * 75
            elif transportation == "biking":
                calories = distance * 40
            print co2
            log = Log(email=email, transportation=transportation, co2=co2, calories=calories, distance=distance, timestamp=str(datetime.datetime.now()))
            print log
            log.put()
            self.redirect('/report')
        else:
            self.redirect('/login')
            #log['error'] = 'User is not logged in.'



class ViewReportHandler(webapp2.RequestHandler):
    def get(self):
        email = get_current_user_email()
        if email:
            q = Log.query().filter(Log.email == email).order(-Log.timestamp)
#            for item in q:
#                print item

            log = q.get()
            if log:
                params = {'transportation': log.transportation ,'distance': log.distance,'calories': log.calories, 'co2': log.co2}
                template = JINJA_ENVIRONMENT.get_template('templates/report.html')
                self.response.write(template.render(params))
            else:
                # redirect to the data form
                self.redirect("/data")
                print 'redirect to the data form'
                pass
        else:
            print "redirect to login"
            pass


class ViewHistoryHandler(webapp2.RequestHandler): #refer to Tim's code in how he
#stored all the data instead of looping through the entire query
    def get(self):
        email = get_current_user_email()
        if email:
            q = Log.query().filter(Log.email == email).order(-Log.timestamp)
            template = JINJA_ENVIRONMENT.get_template('templates/history.html')
            self.response.write(template.render(history=q))
        else:
            print "hi"
    #add in other attributes of the Log class

class Log(ndb.Model):
    email = ndb.StringProperty(required=True)
    distance = ndb.FloatProperty(required=True)
    timestamp = ndb.StringProperty(required=True)
    transportation = ndb.StringProperty(required=True)
    co2 = ndb.FloatProperty(required=True)
    calories = ndb.FloatProperty(required=True)

# class Msg(ndb.Model):
#     email = ndb.StringProperty(required=True)
#     text = ndb.StringProperty(required=True)
#

    def to_dict(self):
        log = {
                'user': self.email,
                'distance': self.distance,
                'timestamp': self.timestamp.strftime('%Y-%m-%d %I:%M:%S'),
                'transportation': self.transportation,
                'co2': self.co2,
                'calories': self.calories
            }
        return log

app = webapp2.WSGIApplication([
	('/', GetUserHandler),
	('/home', GetHomePageHandler),
	('/user', GetUserHandler),
	('/login', GetLoginUrlHandler),
	('/logout', GetLogoutUrlHandler),
	('/data', LogDataHandler),
	('/report', ViewReportHandler), #view your most recent accomplishment
	('/history', ViewHistoryHandler), #views all the progress
    #('/chat', ViewChatHandler)
], debug=True)
