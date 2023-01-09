from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from comments.serializers import CommentSerializer

from comments.models import Comment
from posts.models import Post


class AddCommentAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, format=None):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save(user=request.user, post=post)

        return Response(comment_serializer.data, status=status.HTTP_201_CREATED)