from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from comments.models import Comment
from posts.models import Post

from comments.serializers import CommentSerializer


def add_comment_url(post_id):
    return reverse('comment:add-comment', kwargs={'post_id': post_id})

def comment_update_url(post_id, comment_id):
    return reverse('comment:update-comment', kwargs={'post_id': post_id, 'comment_id': comment_id})

def comment_delete_url(post_id, comment_id):
    return reverse('comment:delete-comment', kwargs={'post_id': post_id, 'comment_id': comment_id})

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
        url = add_comment_url(post.id)
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        


class PrivateCommentTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_if_authorized_user_can_comment_on_posts(self):
        user = get_user_model().objects.create(email='test2@example.com', password='testing123')
        post = Post.objects.create(
            user=user,
            title='Post title',
            body='Something for comment body.'
        )
        payload = {
            'body': 'My first comment on post!!!'
        }
        url = add_comment_url(post.id)
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(post.comments.count(), 1)
        for comment in post.comments.all():
            self.assertEqual(comment.body, 'My first comment on post!!!')

    def test_if_user_can_update_his_comment(self):
        user = get_user_model().objects.create(email='test2@example.com', password='testing123')
        post = Post.objects.create(
            user=user,
            title='Post title',
            body='Something for comment body.'
        )
        comment_1 = Comment.objects.create(user=self.user, post=post, body='My comment..')
        payload = {'body': 'Updated comment'}
        url = comment_update_url(post.id, comment_1.id)
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['body'], 'Updated comment')

    def test_if_user_can_delete_his_comment(self):
        user = get_user_model().objects.create(email='test2@example.com', password='testing123')
        post = Post.objects.create(
            user=user,
            title='Post title',
            body='Something for comment body.'
        )
        comment_1 = Comment.objects.create(user=self.user, post=post, body='My comment..')
        url = comment_delete_url(post.id, comment_1.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_if_user_can_delete_other_users_comments(self):
        user = get_user_model().objects.create(email='test2@example.com', password='testing123')
        post = Post.objects.create(
            user=user,
            title='Post title',
            body='Something for comment body.'
        )
        comment_1 = Comment.objects.create(user=user, post=post, body='My comment..')
        url = comment_delete_url(post.id, comment_1.id)
    
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_if_user_can_update_other_users_comments(self):
        user = get_user_model().objects.create(email='test2@example.com', password='testing123')
        post = Post.objects.create(
            user=user,
            title='Post title',
            body='Something for comment body.'
        )
        comment_1 = Comment.objects.create(user=user, post=post, body='My comment..')
        url = comment_update_url(post.id, comment_1.id)
        payload = {
            'body': 'Trying to update someones comment..'
        }
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    