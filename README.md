[![Build Status](https://travis-ci.org/memespring/open-notices.svg?branch=master)](https://travis-ci.org/memespring/open-notices)

You will need these things:

Python
virtualenv
Postgis (needs to be running)
Redis (needs to be running to send emails)
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
redis-server

source bin/activate
export  DJANGO_SETTINGS_MODULE=open_notices.settings.development
celery -A open_notices worker -l info

##Start the app
source bin/activate
python manage.py runsslserver --settings=open_notices.settings.development

#Send email alerts

source bin/activate
python manage.py sendalerts --settings=open_notices.settings.development
