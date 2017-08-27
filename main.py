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
import requests
from sparkpost import SparkPost
from sendgrid.helpers.mail import *
import jinja2
import re
import webapp2
import os
from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.api import images
import requests_toolbelt.adapters.appengine
from datetime import datetime
from random import randint

requests_toolbelt.adapters.appengine.monkeypatch()
jinja_env = jinja2.Environment(autoescape=True,
                               loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

headers = {"Content-Type": "application/json",
           "Authorization": "Bearer v57wdn8g8ngvjrq2cwmb4cg1vfp6x59c"}


def insert_in_hosts(name, email, phone):
    body = {
        "type": "insert",
        "args": {
            "table": "hosts",
            "objects": [{
                "name": name,
                "email": email,
                "phone": phone
            }]
        }
    }
    url = "https://data.hath50.hasura-app.io/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
    print x.text
    return x.text


def insert_in_checkin(name, email, phone, visitor_id, webcam_pic, host_name, host_email, pic_id="NULL"):
    body = {
        "type": "insert",
        "args": {
            "table": "checkin",
            "objects": [{
                "visitor_name": name,
                "visitor_email": email,
                "visitor_phone": phone,
                "visitor_id": visitor_id,
                "webcam_pic": webcam_pic,
                "host_name": host_name,
                "host_email": host_email,
                "pic_id": pic_id
            }]
        }
    }
    url = "https://data.hath50.hasura-app.io/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
    print x.text
    return x.text


def insert_in_checkout(name, email, phone, visitor_id, webcam_pic, host_name, host_email, pic_id, host_phone,
                       checkin_date):
    body = {
        "type": "insert",
        "args": {
            "table": "checkedout",
            "objects": [{
                "visitor_name": name,
                "visitor_email": email,
                "visitor_phone": phone,
                "visitor_id": visitor_id,
                "webcam_pic": webcam_pic,
                "host_name": host_name,
                "host_email": host_email,
                "pic_id": pic_id,
                "host_phone": host_phone,
                "checkin_date": checkin_date
            }]
        }
    }
    url = "https://data.hath50.hasura-app.io/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
    print x.text
    return x.text


def get_hosts():
    body = {
        "type": "select",
        "args": {
            "table": "hosts",
            "columns": ["*"]
        }
    }
    url = "https://data.hath50.hasura-app.io/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
    print x.text
    return x.text


def get_checkin():
    body = {
        "type": "select",
        "args": {
            "table": "checkin",
            "columns": ["*"]
        }
    }
    url = "https://data.hath50.hasura-app.io/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
    print x.text
    return x.text


def get_checkedout():
    body = {
        "type": "select",
        "args": {
            "table": "checkedout",
            "columns": ["*"]
        }
    }
    url = "https://data.hath50.hasura-app.io/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
    print x.text
    return x.text


def delete_host(email):
    body = {
        "type": "delete",
        "args": {
            "table": "hosts",
            "where": {"email": {"$eq": email}}
        }
    }
    url = "https://data.hath50.hasura-app.io/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
    print x.text
    return x.text


def delete_checkin(visitor_id):
    body = {
        "type": "delete",
        "args": {
            "table": "checkin",
            "where": {"visitor_id": {"$eq": visitor_id}}
        }
    }
    url = "https://data.hath50.hasura-app.io/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
    print x.text
    return x.text


def get_checkin_from_id(visitor_id):
    body = {
        "type": "select",
        "args": {
            "table": "checkin",
            "columns": ["*"],
            "where": {"visitor_id": {"$eq": visitor_id}}
        }
    }
    url = "https://data.hath50.hasura-app.io/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
    print x.text
    return x.text


def get_host_from_email(email):
    body = {
        "type": "select",
        "args": {
            "table": "hosts",
            "columns": ["*"],
            "where": {"email": {"$eq": email}}
        }
    }
    url = "https://data.hath50.hasura-app.io/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
    print x.text
    return x.text


def get_history_from_timestamp(checkin_date, checkout_date):
    body = {
        "type": "select",
        "args": {
            "table": "checkedout",
            "columns": ["*"],
            "where": {
                "$and": [{
                    "checkin_date": {
                        "$gt": checkin_date
                    }
                },
                {
                    "checkin_date": {
                        "$lt": checkout_date
                    }
                }]
            }
        }
    }
    url = "https://data.hath50.hasura-app.io/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
    print x.text
    return x.text


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
    print subject
    print body
    print email
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


def send_simple_email(subject, body, email):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox3044e679dd1947139228f23db8e8d379.mailgun.org/messages",
        auth=("api", "key-5492d5bbddfd085f28cc93268edb72d4"),
        data={"from": "Management <postmaster@sandbox3044e679dd1947139228f23db8e8d379.mailgun.org>",
              "to": "<%s>" % (email),
              "subject": subject,
              "text": body})


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
    visitor_id = db.StringProperty(required=True)
    pic = db.BlobProperty()
    host_name = db.StringProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
    webcam = db.TextProperty()


class CheckedOut(db.Model):
    visitor_name = db.StringProperty(required=True)
    visitor_email = db.StringProperty(required=True)
    visitor_phone = db.StringProperty(required=True)
    visitor_id = db.StringProperty(required=True)
    pic = db.BlobProperty()
    webcam = db.TextProperty()
    host_name = db.StringProperty(required=True)
    host_email = db.StringProperty(required=True)
    host_phone = db.StringProperty(required=True)
    checkin_date = db.DateTimeProperty(required=True)
    checkout_date = db.DateTimeProperty(auto_now_add=True)


class MainHandler(Handler):
    def get(self):
        self.render('welcome.html')


class AddHostHandler(Handler):
    def get(self):
        self.render("registerhost.html", mssg="")

    def post(self):
        name = self.request.get("name")
        if not valid_name(name):
            self.render("registerhost.html", mssg="Invalid Name !!")
            return
        email = self.request.get("email")
        if not valid_email(email):
            self.render("registerhost.html", mssg="Invalid Email !!")
            return
        phone = self.request.get("phone")
        if not valid_phone(phone):
            self.render("registerhost.html", mssg="Invalid Phone Number !!")
            return
        host = Hosts(name=str(name),
                     email=str(email),
                     phone=str(phone)
                     )
        host.put()
        insert_in_hosts(name, email, phone)
        self.redirect('/')


class CheckInHandler(Handler):
    def get(self):
        all_hosts = get_hosts()
        all_hosts = json.loads(all_hosts)
        self.render('checkin.html', hosts=all_hosts, mssg="")

    def post(self):
        all_hosts = get_hosts()
        all_hosts = json.loads(all_hosts)
        name = self.request.get("name")
	print name
        if not valid_name(name):
            self.render("checkin.html", hosts=all_hosts, mssg="Invalid Name !!")
            return
        email = self.request.get("email")
	print email
        if not valid_email(email):
            self.render("checkin.html", hosts=all_hosts, mssg="Invalid Email !!")
            return
        phone = self.request.get("phone")
	print phone
        if not valid_phone(phone):
            self.render("checkin.html", hosts=all_hosts, mssg="Invalid Phone Number !!")
            return
        visitor_id = str(randint(99999, 99999999))
        print visitor_id
        """
        all_checked_in = get_checkin()
        all_checked_in = json.loads(all_checked_in)
        id_found = False
        for i in all_checked_in:
            if visitor_id == i.visitor_id:
                id_found = True
                break
        while id_found:
            visitor_id = str(randint(99999, 99999999))
            id_found = False
            for i in all_checked_in:
                if visitor_id == i.visitor_id:
                    id_found = True
                    break
        print visitor_id
        """
        host_email = self.request.get("host")
	print host_email
        pic = ""
        pic_error = False
        try:
            pic = self.request.get("pic")
            pic = images.resize(pic, 256, 256)
        except:
            print "pic error"
            pic_error = True
            pic = ""
        webcam = ""
        try:
            webcam = self.request.get("webcam")
        except:
            print "webcam error"
            webcam = ""
        webcam_error = False
        if webcam == "":
            webcam_error = True
            # print webcam
        if webcam_error and pic_error:
            self.render("checkin.html", hosts=all_hosts, mssg="Upload a photo or take picture from webcam !!")
            return
        found = False
        host = ""
        all_hosts = get_hosts()
        all_hosts = json.loads(all_hosts)
        for i in all_hosts:
            if i["email"] == host_email:
                found = True
                host = i["name"]
                break

        if found:
            """
            checkin = CheckedIn(visitor_name=str(name),
                                visitor_email=str(email),
                                visitor_phone=str(phone),
                                visitor_id=str(visitor_id),
                                pic=pic,
                                webcam=str(webcam),
                                host_name=str(host)
                                )
            checkin.put()
            """
            if webcam_error:
                # TODO Fix pic ID portion
                insert_in_checkin(name, email, phone, visitor_id, "", host, host_email, "NULL")
            elif pic_error:
                insert_in_checkin(name, email, phone, visitor_id, webcam, host, host_email, "NULL")
            else:
                insert_in_checkin(name, email, phone, visitor_id, webcam, host, host_email, "NULL")
            # checkin_id = str(checkin.key().id())
            body_mssg = ("Name: %s\n\nEmail: %s\n\nPhone: %s\n\n" % (name, email, phone))
            send_simple_email("New Incoming Visitor", body_mssg, host_email)
            self.render("error.html", mssg="Checked In Successfully !", link=visitor_id)
        else:
            self.render("error.html", mssg="Error Checking In !!", link="")


class CheckOutHandler(Handler):
    def get(self):
        all_checkin = get_checkin()
        all_checkin = json.loads(all_checkin)
        self.render("checkout.html", all_checked_in=all_checkin, ids="")

    def post(self):
        visitor_id = self.request.get("visitor_id")
        person_checked_in = get_checkin_from_id(visitor_id)
        person_checked_in = json.loads(person_checked_in)
        ids = []
        # TODO fix image ids to render
        self.render("checkout.html", all_checked_in=person_checked_in, ids=ids)


class CheckedOutHandler(Handler):
    def get(self):
        visitor_id = self.request.get("visitor_id")
        # print visitor_id
        person = get_checkin_from_id(visitor_id)
        # print person
        person = json.loads(person)
        delete_checkin(visitor_id)
        host = get_host_from_email(person[0]["host_email"])
        host = json.loads(host)
        insert_in_checkout(person[0]["visitor_name"], person[0]["visitor_email"], person[0]["visitor_phone"],
                           person[0]["visitor_id"], person[0]["webcam_pic"], person[0]["host_name"],
                           person[0]["host_email"], person[0]["pic_id"], host[0]["phone"], person[0]["created"])
        name = person[0]["visitor_name"]
        email = person[0]["visitor_email"]
        host_mail = person[0]["host_email"]
        send_simple_email("Visitor Checked Out !!", "Name:%s\n\nEmail: %s\n\n" % (name, email), host_mail)
        self.render("error.html", mssg="Checked Out Successfully !!", link="")


class ImgHandler(Handler):
    def get(self):
        check_in_id = self.request.get("id")
        key = db.Key.from_path('CheckedOut', int(check_in_id))
        person = db.get(key)
        if person.pic:
            self.response.headers['Content-Type'] = 'image/jpeg'
            self.response.out.write(person.pic)
        else:
            self.response.out.write('No image')


class ImageHandler(Handler):
    def get(self):
        check_in_id = self.request.get("id")
        key = db.Key.from_path('CheckedIn', int(check_in_id))
        person = db.get(key)
        if person.pic:
            self.response.headers['Content-Type'] = 'image/jpeg'
            self.response.out.write(person.pic)
        else:
            self.response.out.write('No image')


class PermalinkHandler(Handler):
    def get(self):
        person_id = self.request.get("id")
        print person_id
        person = get_checkin_from_id(person_id)
        person = json.loads(person)
        self.render("permalink.html", i=person, id=person_id)


class ReportHandler(Handler):
    def get(self):
        self.render("report.html", history="", ids="")

    def post(self):
        start_day = int(self.request.get("sday"))
        start_month = int(self.request.get("smonth"))
        start_year = int(self.request.get("syear"))
        end_day = int(self.request.get("eday"))
        end_month = int(self.request.get("emonth"))
        end_year = int(self.request.get("eyear"))
        start_datetime = datetime(start_year, start_month, start_day)
        end_datetime = datetime(end_year, end_month, end_day)
        ids = []
        all_history = get_history_from_timestamp(str(start_datetime), str(end_datetime))
        all_history = json.loads(all_history)
        self.render("report.html", history=all_history, ids=ids)


class TestHandler(Handler):
    def get(self):
        self.render("index.html")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/addhost', AddHostHandler),
    ('/checkin', CheckInHandler),
    ('/checkout', CheckOutHandler),
    ('/checkedout', CheckedOutHandler),
    ('/image', ImageHandler),
    ('/img', ImgHandler),
    ('/permalink', PermalinkHandler),
    ('/generatereport', ReportHandler),
    ('/test', TestHandler)
], debug=True)
