from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


USER_CREATE_URL = reverse("user:create")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class CreateUserTests(TestCase):
    """Tests for User Creation"""
    def setUp(self):
        self.client = APIClient()

    def test_if_user_can_be_created_by_email(self):
        payload = {
            'email': 'test@test.bk',
            'password': 'test12345'
        }
        response = self.client.post(USER_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.filter(email=payload.get('email')).first()
        self.assertTrue(user.check_password(payload.get('password')))
        self.assertNotIn('password', response.data)
