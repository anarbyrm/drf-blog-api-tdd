from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from posts import views, serializers, models


POST_LIST_URL = reverse('post:post-list')



def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


def create_post(user):
    post= models.Post.objects.create(
        user=user,
        title='Post title',
        body='Post body'
    )
    return post


class PublicPostApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()


    def test_if_post_list_can_be_seen_by_unauthenticated_user(self):
        user = create_user(email='testuser@example.com', password='testing123')
        post_1 = create_post(user=user)
        post_2 = create_post(user=user)
        post_3 = create_post(user=user)
        response = self.client.get(POST_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthenticatedUserPostApiTests(TestCase):
    def setUp(self):
        self.user = create_user(email='testuser@example.com', password='testing123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

