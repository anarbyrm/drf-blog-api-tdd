from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from comments.models import Comment
from posts.models import Post


def comment_url(post_id):
    return reverse('comment:add-comment', args=[post_id])

def create_user():
    email = 'test@example.com'
    password = 'testing123'
    user = get_user_model().objects.create(
        email=email,
    )
    user.set_password(password)
    return user


class PublicCommentTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_if_unauthorized_user_can_comment_on_posts(self):
        user = create_user()
        post = Post.objects.create(
            user=user,
            title='Post title',
            body='Something for comment body.'
        )
        payload = {
            'body': 'My first comment on post!!!'
        }
        url = comment_url(post.id)
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        


class PrivateCommentTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    
    