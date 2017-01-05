[![Build Status](https://travis-ci.org/memespring/open-notices.svg?branch=master)](https://travis-ci.org/memespring/open-notices)

#Open Notices

Open Notices is a platform for publishing civic notices that apply to a specific geography for a fixed time &mdash; things like planning applications, local consultations or items needed by a food bank.

Anyone can publish a notice (think of it like Wikipedia for civic information), but local government and other organisations can ask to be verified to make it clear which notices that have come directly from them, and which have been submitted by the public.

It's not about publishing text though. Open Notices makes it easy to make notices available as structured data, via a decent API.

This makes it easier to add civic notices to community websites, to apps, or even printed on receipts in a local cafe.

(There is a basic alerts service too - you can just draw the outline of the neighbourhood you are interested in on a map and you'll receive an email every time there is a new notice in that area- but hopefully most people won't use it in the long-run.)

##Getting development version running

You will need these things installed:

* Python
* virtualenv
* Postgres
* Redis
* Grunt

todo: add instructions for setting up database (hstore and postgis)

###Get the code:

git clone https://github.com/memespring/open-notices.git
virtualenv .

###Run tests
source bin/activate
python manage.py test notices alerts core --settings=open_notices.settings.test

###Start SCSS compiler
npm install
$ grunt

###Start the message queue
redis-server

source bin/activate
export  DJANGO_SETTINGS_MODULE=open_notices.settings.development
celery -A open_notices worker -l info

###Start the app
source bin/activate
python manage.py runsslserver --settings=open_notices.settings.development

###Send email alerts

source bin/activate
python manage.py sendalerts --settings=open_notices.settings.development
