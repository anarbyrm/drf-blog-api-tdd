from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


USER_CREATE_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
PROFILE_URL = reverse("user:profile")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserTests(TestCase):
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

    def test_if_unauthorized_user_can_see_user_profile(self):
        response = self.client.get(PROFILE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    

class AuthorizedUserTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email='authedtest@example.com',
            password='authedtest12345'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_if_authorized_user_can_see_his_profile(self):
        response = self.client.get(PROFILE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_user_can_post_to_profile_endpoint(self):
        payload = {
            'email': 'test@example.com',
            'password': 'testing123' 
        }
        response = self.client.post(PROFILE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_if_user_can_update_his_profile(self):
        payload = {'email': 'newtest@test.com', 'password': 'newpassword123'}
        response_patch = self.client.patch(PROFILE_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, payload['email'])
        self.assertTrue(self.user.check_password(payload['password']))

