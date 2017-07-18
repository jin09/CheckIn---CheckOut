import requests
import json

headers = {"Content-Type": "application/json",
           "Authorization": "Bearer vuiu77u8ivm1gugwxyf06yhi8heofu7p"}

body = {
    "type": "insert",
    "args": {
        "table": "hosts",
        "objects": [{
            "name": "Gautam Jain",
            "email": "gautam.jain9@yahoo.com",
            "phone": "9818002587"
        }]
    }
}

url = "http://data.c100.hasura.me/v1/query"

x = requests.post(url, data=json.dumps(body), headers=headers)

print x.text