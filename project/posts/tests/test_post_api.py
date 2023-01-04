from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from rest_framework.test import APIClient
from rest_framework import status

from posts import views, serializers, models


POST_LIST_URL = reverse('post:post-list')

def post_detail_url(post_id):
    return reverse('post:post-detail', args=[post_id])


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
        for _ in range(3):
            create_post(user=user)
        response = self.client.get(POST_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_unauthenticated_user_can_create_posts(self):
        user = create_user(email='testuser@example.com', password='testing123')
        try:
            response = self.client.post(POST_LIST_URL, {'title': 'new post', 'body': 'post body'})
        except:
            self.failureException(ValueError)

    def test_if_unauthenticated_user_can_manage_someones_posts(self):
        user = create_user(email='testuser@example.com', password='testing123')
        post = create_post(
            user=user
        )
        url = post_detail_url(post.id)
        response = self.client.put(url, data={'title': 'Updated title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(post.title, 'Updated title')


class AuthenticatedUserPostApiTests(TestCase):
    def setUp(self):
        self.user = create_user(email='testuser@example.com', password='testing123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_if_user_can_create_posts(self):
        payload = {'title': 'new post', 'body': 'post body'}
        response = self.client.post(POST_LIST_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in payload.items():
            self.assertEqual(response.data[key], value)


    def test_if_user_can_update_his_posts(self):
        post = create_post(user=self.user)
        url = post_detail_url(post.id)
        response = self.client.patch(url, {'title': 'Updated!'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated!')

    def test_if_user_can_delete_his_posts(self):
        post = create_post(user=self.user)
        url = post_detail_url(post.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_if_user_can_update_someones_post(self):
        user = create_user(email='test@example.com', password='testing123')
        post = create_post(user=user)
        url = post_detail_url(post.id)
        response = self.client.patch(url, {'title': 'Updated someones post'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_user_can_delete_someones_post(self):
        user = create_user(email='test@example.com', password='testing123')
        post = create_post(user=user)
        url = post_detail_url(post.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        