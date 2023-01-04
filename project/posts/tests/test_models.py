from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from posts.models import Post

def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PostModel(TestCase):
    def test_if_model_object_can_be_created(self):
        user = create_user(email='test@example.com', password='test12345')
        post = Post(
            user=user,
            title='Post title',
            body='Post body'
        )

        self.assertEqual(str(post), post.title)