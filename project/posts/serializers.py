from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'title']
        read_only_fields = ['id', 'user', 'created_at']


class PostDetailSerializer(serializers.ModelSerializer):
     class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'body', 'created_at', 'slug']
        read_only_fields = ['id', 'user', 'created_at']
