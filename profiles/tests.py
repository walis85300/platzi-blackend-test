from django.test import TestCase
from django.test import Client

from django.contrib.auth.models import User
# Create your tests here.


class LoginTest(TestCase):

    def SetUp(self):
        self.client = Client()

    def test_login(self):
        self.user = User.objects.create_user(
            username='admin', password='pass@123', email='admin@admin.com')
        response = self.client.login(username='admin', password='pass@123')
        self.assertTrue(response)

    def test_logout(self):
        User.objects.create_user(
            username='admin', password='pass@123', email='admin@admin.com')
        self.client.login(username='admin', password='pass@123')
        self.client.logout()

    def test_signup(self):
        response = self.client.post('/users/signup/', {
            'username': 'testusername',
            'password': '123456',
            'password_confirmation': '123456',
            'first_name': 'test',
            'last_name': 'last test',
            'email': 'test@test.com',
            'website': 'https://testsite.dev',
            'phone_number': '123456',
            'stripe_token': 'tok_visa'},
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/users/login/')

    def test_signup_fail(self):
        response = self.client.post('/users/signup/', {
            'username': 'testusernamef',
            'password': '123456',
            'password_confirmation': '1233456',
            'first_name': 'test',
            'last_name': 'last test',
            'email': 'test@test.com',
            'website': 'https://testsite.dev',
            'phone_number': '123456',
            'stripe_token': 'tok_visa'},
            follow=False)

        self.assertEqual(response.status_code, 200)
