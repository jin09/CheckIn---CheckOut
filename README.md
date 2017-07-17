# CheckIn---CheckOut

Installation instructions for Linux

One time
git clone https://github.com/jin09/CheckIn---CheckOut.githttps://github.com/jin09/CheckIn---CheckOut.git
wget -O ~/gapp.zip "https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.57.zip" && sudo apt-get install unzip && sudo unzip ~/gapp.zip sudo rm -f gapp.zip

Runserver
python ~/google_appengine/dev_appserver.py [path/to/project/app.yaml]
