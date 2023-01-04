from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'title']


class PostDetailSerializer(serializers.ModelSerializer):
     class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'body', 'created_at', 'slug']
