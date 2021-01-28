from django.test import TestCase
from django.urls import reverse



class BaseTest(TestCase):
    def setUp(self):
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        self.user={
            'username': 'ime2@domena.com',
            'email': 'ime2@domena.com',
            'password': 'Datulja2222',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'opg_name': 'opg_name',
            'address': 'address',
            'phone': 'phone',
        }

        return super().setUp()


class RegisterTest(BaseTest):

    def test_can_register_user(self):
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,302)

