from rest_framework import serializers

from .models import Post
from comments.serializers import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'title']
        read_only_fields = ['id', 'user', 'created_at']


class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'body', 'comments', 'created_at', 'slug']
        read_only_fields = ['id', 'user', 'created_at']

