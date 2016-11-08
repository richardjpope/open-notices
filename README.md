![Build Status](https://travis-ci.org/memespring/open-notices.svg?branch=master)

You will need these things:

Python
virtualenv
Postgis (needs to be running)
RabitMQ (needs to be running)
Grunt

#Run development version
git clone https://github.com/memespring/open-notices.git
virtualenv .

##Run tests
source bin/activate
python manage.py test notices alerts core --settings=community.settings.test

##Start SCSS compiler
npm install
$ grunt

##Start the message queue
source bin/activate
celery -A community worker -l info

##Start the app
source bin/activate
python manage.py runserver --settings=community.settings.development
