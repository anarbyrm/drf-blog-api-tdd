from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from posts.models import Post
from comments.models import Comment


def create_user():
    email = 'test@example.com'
    password = 'testing123'
    user = get_user_model().objects.create(
        email=email,
    )
    user.set_password(password)
    return user


class CommentModelTests(TestCase):
    def test_if_comment_model_object_can_be_created(self):
        user = create_user()
        post = Post.objects.create(
            user=user,
            title='Post title',
            body='Something for comment body.'
        )
        comment = Comment.objects.create(
            user=user,
            post=post,
            body='It is awesome!' 
        )
        exists = Comment.objects.all().exists()
        self.assertTrue(exists)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(comment.body, "It is awesome!")
