import requests
import json
from datetime import datetime

headers = {"Content-Type": "application/json",
           "Authorization": "Bearer vuiu77u8ivm1gugwxyf06yhi8heofu7p"}


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
    url = "http://data.c100.hasura.me/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
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
    url = "http://data.c100.hasura.me/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
    return x.text


def insert_in_checkout(name, email, phone, visitor_id, webcam_pic, host_name, host_email, pic_id, host_phone,
                       checkin_date, checkout_date):
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
                "checkin_date": checkin_date,
                "checkout_date": checkout_date
            }]
        }
    }
    url = "http://data.c100.hasura.me/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
    return x.text


def get_hosts():
    body = {
        "type": "select",
        "args": {
            "table": "hosts",
            "columns": ["*"]
        }
    }
    url = "http://data.c100.hasura.me/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
    return x.text


def get_checkin():
    body = {
        "type": "select",
        "args": {
            "table": "checkin",
            "columns": ["*"]
        }
    }
    url = "http://data.c100.hasura.me/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
    return x.text


def get_checkedout():
    body = {
        "type": "select",
        "args": {
            "table": "checkedout",
            "columns": ["*"]
        }
    }
    url = "http://data.c100.hasura.me/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
    return x.text


def delete_host(email):
    body = {
        "type": "delete",
        "args": {
            "table": "hosts",
            "where": {"email": {"$eq": email}}
        }
    }
    url = "http://data.c100.hasura.me/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
    return x.text


def delete_checkin(visitor_id):
    body = {
        "type": "delete",
        "args": {
            "table": "checkin",
            "where": {"visitor_id": {"$eq": visitor_id}}
        }
    }
    url = "http://data.c100.hasura.me/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
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
    url = "http://data.c100.hasura.me/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
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
    url = "http://data.c100.hasura.me/v1/query"
    x = requests.post(url, data=json.dumps(body), headers=headers)
    return x.text

def upload_image(pic):
    pass


x = get_history_from_timestamp(str(datetime(2017, 6, 30)), str(datetime(2017, 7, 25)))
print x
