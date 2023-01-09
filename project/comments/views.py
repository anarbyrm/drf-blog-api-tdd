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

    def post(self, request, post_id, format=None):
        post = get_object_or_404(Post, id=post_id)

        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save(user=request.user, post=post)

        return Response(comment_serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, post_id, comment_id, format=None):
        post = get_object_or_404(Post, id=post_id)
        comment = post.comments.filter(id=comment_id)
        if comment.exists():
            comment = comment.first()
            if comment.user == request.user:
                serializer = CommentSerializer(comment, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': "Comment doesn't exist"})

    def delete(self, request, post_id, comment_id, format=None):
        post = get_object_or_404(Post, id=post_id)
        comment = post.comments.filter(id=comment_id)
        if comment.exists():
            comment = comment.first()
            if comment.user == self.request.user:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': "Comment doesn't exist"})