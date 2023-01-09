from django.db import models
from django.conf import settings

from posts.models import Post

User = settings.AUTH_USER_MODEL


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} on post: {self.post} - "{self.body}"'
        
