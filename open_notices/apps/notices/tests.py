from django.test import TestCase
from django.test import Client
from rest_framework.test import APIClient
from notices import models
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from datetime import datetime

class NoticeModelTestCase(TestCase):

    def setUp(self):
        UserModel = get_user_model()
        self.user = UserModel(email='existinguser@example.org')
        self.user.set_password('notasecret')
        self.user.save()

    def test_invalid_date_range(self):
        with self.assertRaises(ValidationError):
            notice = models.Notice()
            notice.title = 'test title'
            notice.details = 'test details'
            notice.location = 'SRID=3857;POINT (-284821.3533571999869309 6865433.3731604004278779)'
            notice.starts_at = datetime(2016, 1, 1)
            notice.ends_at = datetime(2012, 1, 1)
            notice.timezone = "Europe/London"
            notice.user = self.user
            notice.save()

class NoticeAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        UserModel = get_user_model()
        self.user = UserModel(email='existinguser@example.org')
        self.user.set_password('notasecret')
        self.user.save()
        Token.objects.create(user=self.user)

    def get_valid_data(slef):
        return {'title': 'test title', 'location': {"type":"Point","coordinates":[-0.09430885313565737,51.43326585306407]}, 'data': [],"starts_at":"2016-01-01T11:00:00","ends_at":"2016-01-02T12:00:00", "timezone": "Europe/London"}

    def test_create_get_not_found(self):
        response = self.client.get('/notices/new.json')
        self.assertEqual(response.status_code, 405)

    def test_create_unauthorised(self):
        response = self.client.post('/notices/new.json')
        self.assertEqual(response.status_code, 401)

    def test_create_authorised_empty(self):
        token = Token.objects.get_or_create(user=self.user)[0]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post('/notices/new.json')
        self.assertEqual(response.status_code, 400)

    def test_create_authorised_valid(self):
        data = self.get_valid_data()
        token = Token.objects.get_or_create(user=self.user)[0]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post('/notices/new.json', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_non_json_denied(self):
        data = self.get_valid_data()
        token = Token.objects.get_or_create(user=self.user)[0]

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post('/notices/new.geojson', data, format='json')
        self.assertEqual(response.status_code, 405)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post('/notices/new.csv', data, format='json')
        self.assertEqual(response.status_code, 405)

class NoticeTestCase(TestCase):
    def setUp(self):

        # Every test needs a client.
        self.client = Client()

        #create a user for use later
        UserModel = get_user_model()
        self.user = UserModel(email='existinguser@example.org')
        self.user.set_password('notasecret')
        self.user.save()

    def test_list(self):
        response = self.client.get('/notices/')
        self.assertEqual(response.status_code, 200)

    def test_view_notice(self):
        notice = models.Notice()
        notice.title = 'test title'
        notice.details = 'test details'
        notice.location = 'SRID=3857;POINT (-284821.3533571999869309 6865433.3731604004278779)'
        notice.starts_at = datetime(2016, 1, 1)
        notice.ends_at = datetime(2016, 1, 1)
        notice.timezone = "Europe/London"
        notice.user = self.user
        notice.save()

        response = self.client.get('/notices/%s/' % notice.pk)

        self.assertContains(response, 'test title', 2, 200)
        self.assertEqual(response.status_code, 200)

    def test_create_unauthorised(self):
        response = self.client.post('/notices/new', follow=True)
        self.assertRedirects(response, '/signin/?next=/notices/new')

    def test_create_empty(self):
        self.client.login(email='existinguser@example.org', password='notasecret')
        response = self.client.post('/notices/new')
        self.assertContains(response, "This field is required", 4, 200)
        self.assertContains(response, "No geometry value provided", 1, 200)

    def test_create_valid(self):
        self.client.login(email='existinguser@example.org', password='notasecret')
        data =  {'title': 'Test notice', 'details': 'It is a test', 'location': 'SRID=3857;POINT (-284821.3533571999869309 6865433.3731604004278779)', 'starts_at': '2016-01-01', 'ends_at': '2016-01-02', 'timezone': 'Europe/London'}
        response = self.client.post('/notices/new', data)

        self.assertEqual(response.status_code, 302)