from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Tests for User models"""
    def test_if_user_can_be_created_by_email(self):
        """Tests if user object can be created by email"""
        email = 'test@example.com'
        password = 'mypassword'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.email, email)
    
    def test_if_superuser_can_be_created_by_email(self):
        email = 'superuser@example.com'
        password = 'test12345'
        user = get_user_model().objects.create_superuser(
            email=email,
            password= password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)