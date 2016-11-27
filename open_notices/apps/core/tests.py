from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

class APITokenTestCase(TestCase):
    def setUp(self):

        # Every test needs a client.
        self.client = Client()

        #create a user for use later
        UserModel = get_user_model()
        self.user = UserModel(email='existinguser@example.org')
        self.user.set_password('notasecret')
        self.user.save()

    def test_create_account_redirect_safe(self):
        unsafe_url = '/create-account?next=http://example.org'
        data = {'email': 'newuser@example.org', 'password': 'notasecret'}
        response = self.client.post(unsafe_url, data, follow=True)
        self.assertRedirects(response, '/')


    def test_unauthenticated(self):
        response = self.client.get('/api')
        self.assertContains(response, "Sign in</a> to create an API key", 1, 200)

    def test_unauthenticated_post(self):
        response = self.client.post('/api')
        self.assertEqual(response.status_code, 404)

    def test_authenticated(self):
        self.client.login(email='existinguser@example.org', password='notasecret')
        response = self.client.get('/api')
        self.assertContains(response, "You do not have an API key", 1, 200)

    def test_generate(self):
        self.client.login(email='existinguser@example.org', password='notasecret')

        response = self.client.post('/api', {'generate': 'generate'})
        token = Token.objects.filter(user=self.user).first()

        self.assertContains(response, token, 1, 200)


    def test_regenerate(self):
        self.client.login(email='existinguser@example.org', password='notasecret')

        response = self.client.post('/api', {'generate': 'generate'})
        token_1 = Token.objects.filter(user=self.user).first()

        response = self.client.post('/api', {'regenerate': 'regenerate'})
        token_2 = Token.objects.filter(user=self.user).first()

        self.assertNotEqual(token_1, token_2)

        self.assertContains(response, token_2, 1, 200)
