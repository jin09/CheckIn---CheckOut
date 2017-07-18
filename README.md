# Checkin---Checkout

Automating visitor management system to keep the workspace safe and secure for everyone. Aim is to provide best hospitality services to office visitors and managing their entry and exit

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Linux Environment (Tested on Ubuntu)
Python
```

### Installing

Get a copy of this repository
```
git clone https://github.com/jin09/CheckIn---CheckOut.git
```

One time setup

```
sudo wget -O ~/gapp.zip "https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.57.zip"
sudo unzip ~/gapp.zip
sudo rm -f ~/gapp.zip
```
Deploy Server Locally

```
python ~/google_appengine/dev_appserver.py [path/to/project/app.yaml]
```

If this project repository is in your home folder then last command would look something like
```
python ~/google_appengine/dev_appserver.py ~/CheckIn---CheckOut/app.yaml
```
