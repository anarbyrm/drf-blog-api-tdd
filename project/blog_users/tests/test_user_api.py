from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


USER_CREATE_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class UserTests(TestCase):
    """Tests for User Creation"""
    def setUp(self):
        self.client = APIClient()

    def test_if_user_can_be_created(self):
        payload = {
            'email': 'test@test.bk',
            'password': 'test12345'
        }
        response = self.client.post(USER_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.filter(email=payload.get('email')).first()
        self.assertTrue(user.check_password(payload.get('password')))
        self.assertNotIn('password', response.data)

    def test_if_token_can_be_created(self):
        credentials = {
            'email': 'test@example.com',
            'password': 'testing123'
        }
        create_user(**credentials)
        payload = {
            'email': credentials['email'],
            'password': credentials['password']
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
    
    def test_if_bad_email_for_token_is_accepted(self):
        credentials = {
            'email': 'test@example.com',
            'password': 'testing123'
        }
        create_user(**credentials)
        payload = {
            'email': 'testexample.com', #bad email address
            'password': 'testing123'
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_if_bad_password_for_token_is_accepted(self):
        credentials = {
            'email': 'test@example.com',
            'password': 'testing123'
        }
        create_user(**credentials)
        payload = {
            'email': 'test@example.com', 
            'password': ''  # bad password
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    