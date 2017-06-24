#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import json
import logging
import urllib
import sendgrid
from sendgrid.helpers.mail import *
import jinja2
import re
import webapp2
import os
from google.appengine.api import mail
from google.appengine.api import urlfetch
from google.appengine.ext import db
import webapp2


jinja_env = jinja2.Environment(autoescape=True,
                               loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))


USER_RE = re.compile(r"^[a-zA-Z]{3,20}\s?([a-zA-Z]{3,20})?$")


def valid_name(username):
    if username and USER_RE.match(username):
        return True
    else:
        return False


EMAIL_RE = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def valid_email(email):
    if email and EMAIL_RE.match(email):
        return True
    else:
        return False


def valid_phone(phone):
    if phone.isdigit() and len(phone) == 10:
        return True
    else:
        return False


def send_simple_message(subject, body, email):
    SENDGRID_API_KEY = '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'
    SENDGRID_SENDER = 'gautam.jain9@yahoo.com'
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
    from_email = Email(SENDGRID_SENDER)
    subject = subject
    to_email = Email(email)
    content = Content("text/plain", body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
    return response.body


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Hosts(db.Model):
    name = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    phone = db.StringProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)


class CheckedIn(db.Model):
	visitor_name = db.StringProperty(required=True)
	visitor_email = db.StringProperty(required=True)
	visitor_phone = db.StringProperty(required=True)
	host_name = db.StringProperty(required=True)
	date = db.DateTimeProperty(auto_now_add=True)


class MainHandler(Handler):
    def get(self):
        self.response.write('Hello world!')


class AddHostHandler(Handler):
    def post(self):
        name = self.request.get("name")
        email = self.request.get("email")
        phone = self.request.get("phone")
        host = Hosts(name=str(name),
                     email=str(email),
                     phone=str(phone)        
                    )
        host.put()
        self.redirect('/')


class CheckInHandler(Handler):
    def post(self):
        name = self.request.get("name")
        email = self.request.get("email")
        phone = self.request.get("phone")
        host = self.request.get("host")

        found = False
        host_email = ""
        all_hosts = db.GqlQuery("select * from Hosts")
        for i in all_hosts:
        	if i.name == host:
        		found = True
        		host_email = i.email
        		break

        if found:
	        checkin = CheckedIn(visitor_name=str(name),
	                     visitor_email=str(email),
	                     visitor_phone=str(phone),
	                     host_name = str(host)        
	                    )
	        checkin.put()
	        body_mssg = ("Name: %s\n\nEmail: %s\n\nPhone: %s\n\n"%(name, email, phone))
	        send_simple_message("New Incoming Visitor", body_mssg, host_email)
	        self.render("error.html", mssg="Checked In Successfully !")
	    else:
	    	self.render("error.html", mssg="Error Checking In !!")


class CheckOutHandler(Handler):
	def get(self):
		all_checked_in = db.GqlQuery("select * from CheckedIn")
		self.render("checkedin.html", all_checked_in=all_checked_in)

	def post(self):
		name = self.request.get("name")
		email = self.request.get("email")
		all_checked_in = db.GqlQuery("select * from CheckedIn")
		
		found = False
		for i in all_checked_in:
			if i.visitor_name == name and i.visitor_email == email:
				found = True
				i.delete()
				break
		if found:
			self render("error.html", mssg="Checked Out Successfully !!")
		if not found:
			self.render("error.html", mssg="no such person checked in !!")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/addhost', AddHostHandler),
    ('/checkin', CheckInHandler),
    ('/checkout', CheckOutHandler)
], debug=True)
