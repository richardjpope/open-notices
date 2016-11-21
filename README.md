[![Build Status](https://travis-ci.org/memespring/open-notices.svg?branch=master)](https://travis-ci.org/memespring/open-notices)

You will need these things:

Python
virtualenv
Postgis (needs to be running)
RabitMQ (needs to be running to send emails)
Grunt

#todo: instructions for setting up database (hstore and postgis)

#Run development version
git clone https://github.com/memespring/open-notices.git
virtualenv .

##Run tests
source bin/activate
python manage.py test notices alerts core --settings=open_notices.settings.test

##Start SCSS compiler
npm install
$ grunt

##Start the message queue
source bin/activate
celery -A open_notices worker -l info

##Start the app
source bin/activate
python manage.py runserver --settings=open_notices.settings.development
