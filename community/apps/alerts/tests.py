from django.test import TestCase
from django.test import Client
from main.models import User

class AlertTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testbot', email='test@example.org', password='notasecret')

    def test_create_unauthorised(self):
        response = self.client.post('/alerts/new', follow=True)
        self.assertRedirects(response, '/signin/?next=/alerts/new')