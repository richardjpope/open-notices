![Build Status](https://travis-ci.org/memespring/open-notices.svg?branch=master)

You will need these things:

Python 3
Postgis (needs to be running)
RabitMQ (needs to be running)
Grunt

#Run tests
python manage.py test notices alerts main --settings=community.settings.test

#Run development version

##Start SCSS compiler
npm install
$ grunt

##Start the message queue
source bin/activate
celery -A community worker -l info

##Start the app
source bin/activate
python manage.py runserver --settings=community.settings.development
