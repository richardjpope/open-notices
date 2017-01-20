import json
from django.test import TestCase
from django.test import Client
from rest_framework.test import APIClient
from django.conf import settings
from django.contrib.auth import get_user_model
from alerts import models

geojson_area = '{"type":"Polygon","coordinates":[[[-12994.086760352204,6704101.992230969],[-12994.086760352204,6703614.309621244],[-12978.847116174482,6703279.028118642],[-12963.60747199676,6703279.028118642],[-12948.367827819038,6703279.028118642],[-12902.648895285873,6703279.028118642],[-12826.446009051298,6703279.028118642],[-12765.487432340411,6703279.028118642],[-12658.805257750391,6703279.028118642],[-12552.123083160373,6703279.028118642],[-12460.685218094042,6703279.028118642],[-12369.242687681746,6703279.028118642],[-12323.52375514858,6703279.028118642],[-12247.320868914006,6703279.028118642],[-12201.601936380841,6703279.028118642],[-12155.883003847674,6703279.028118642],[-12125.399050146265,6703279.028118642],[-12110.159405968545,6703263.783809119],[-12094.919761790821,6703263.783809119],[-12079.680117613101,6703263.783809119],[-12064.440473435377,6703263.783809119],[-12064.440473435377,6703279.028118642],[-12064.440473435377,6703309.5074069975],[-12064.440473435377,6703339.986695353],[-12079.680117613101,6703385.705627887],[-12079.680117613101,6703431.429225765],[-12094.919761790821,6703507.627446654],[-12094.919761790821,6703568.590688711],[-12094.919761790821,6703629.549265422],[-12094.919761790821,6703675.268197955],[-12094.919761790821,6703720.991795834],[-12094.919761790821,6703766.710728367],[-12094.919761790821,6703812.4296609005],[-12094.919761790821,6703858.148593433],[-12094.919761790821,6703888.6325471345],[-12094.919761790821,6703919.11183549],[-12094.919761790821,6703934.351479668],[-12094.919761790821,6703949.591123845],[-12094.919761790821,6703964.830768024],[-12094.919761790821,6703980.070412201],[-12094.919761790821,6703995.310056379],[-12094.919761790821,6704010.554365902],[-12110.159405968545,6704025.79401008],[-12110.159405968545,6704041.033654258],[-12110.159405968545,6704056.273298436],[-12110.159405968545,6704071.512942613],[-12110.159405968545,6704086.752586791],[-12110.159405968545,6704101.992230969],[-12110.159405968545,6704117.231875147],[-12994.086760352204,6704101.992230969]]]}'

class AlertAPIGeojsonTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        
        #create a user for use later
        UserModel = get_user_model()
        self.user = UserModel(email='existinguser@example.org')
        self.user.set_password('notasecret')
        self.user.save()

    def test_list(self):
        response = self.client.get('/alerts.geojson')
        self.assertEqual(response.status_code, 401)

        self.client.login(email='existinguser@example.org', password='notasecret')

        response = self.client.get('/alerts.geojson')
        self.assertEqual(response.status_code, 200)

    def test_create_method_not_allowed(self):
        
        self.client.login(email='existinguser@example.org', password='notasecret')
        data =  {'location': json.loads(geojson_area)}
        response = self.client.post('/alerts/new.geojson', data, format='json')
        self.assertEqual(response.status_code, 405)

class AlertAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        #create a user for use later
        UserModel = get_user_model()
        self.user = UserModel(email='existinguser@example.org')
        self.user.set_password('notasecret')
        self.user.save()

    def test_list(self):

        response = self.client.get('/alerts.json')
        self.assertEqual(response.status_code, 401)

        self.client.login(email='existinguser@example.org', password='notasecret')

        response = self.client.get('/alerts.json')
        self.assertEqual(response.status_code, 200)

    def test_detail(self):

        alert = models.Alert()
        alert.location = geojson_area
        alert.user = self.user
        alert.save()

        response = self.client.get('/alerts/%s.json' % alert.id)
        self.assertEqual(response.status_code, 401)

        self.client.login(email='existinguser@example.org', password='notasecret')

        response = self.client.get('/alerts/%s.json' % alert.id)
        self.assertEqual(response.status_code, 200)

        UserModel = get_user_model()
        user = UserModel(email='anotheruser@example.org')
        user.set_password('notasecret')
        user.save()

        self.client.login(email='anotheruser@example.org', password='notasecret')

        response = self.client.get('/alerts/%s.json' % alert.id)
        self.assertEqual(response.status_code, 403)

    def test_create_unauthorised(self):
        response = self.client.post('/alerts/new.json', format='json')
        self.assertEqual(response.status_code, 401)

    def test_create_authorised(self):
        self.client.login(email='existinguser@example.org', password='notasecret')
        data =  {'location': json.loads(geojson_area)}
        response = self.client.post('/alerts/new.json', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_invalid(self):
        self.client.login(email='existinguser@example.org', password='notasecret')
        data =  {'some': 'thing'}
        response = self.client.post('/alerts/new.json', data, format='json')
        self.assertEqual(response.status_code, 400)

class AlertTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        #create a user for use later
        UserModel = get_user_model()
        self.user = UserModel(email='existinguser@example.org')
        self.user.set_password('notasecret')
        self.user.save()

    def test_create_empty(self):

        data =  {'location': ''}

        response = self.client.post('/alerts/new', data)
        self.assertContains(response, 'Please select an area by drawing on the map')

    def test_create_invalid(self):

        data =  {'location': 'not a polygon'}

        response = self.client.post('/alerts/new', data)
        self.assertContains(response, 'Invalid area selected')

    def test_create_unauthorised(self):

        data =  {'location': geojson_area}

        response = self.client.post('/alerts/new', data, follow=True)
        self.assertRedirects(response, '/alerts/new/account')

        data = {'email': 'newuser@example.com', 'password': 'notasecret'}
        response = self.client.post('/alerts/new/account', data, follow=True)
        self.assertRedirects(response, '/alerts')

        response = self.client.get('/alerts')
        
        # self.assertContains(response, 'Your alert has been created')


    def test_create_authorised(self):

        self.client.login(email='existinguser@example.org', password='notasecret')

        data =  {'location': geojson_area}
        response = self.client.post('/alerts/new', data, follow=True)
        self.assertRedirects(response, '/alerts')

        response = self.client.get('/alerts')
        # self.assertContains(response, 'Your alert has been created')

    def test_create_delete(self):

        self.client.login(email='existinguser@example.org', password='notasecret')

        alert = models.Alert()
        alert.location = geojson_area
        alert.user = self.user
        alert.save()

        data = {'delete': 'yes'}
        response = self.client.post('/alerts/%s/delete' % alert.id, data, follow=True)

        self.assertNotContains(response, "Delete this alert")
        
