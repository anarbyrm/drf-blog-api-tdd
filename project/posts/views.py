from rest_framework.viewsets import ModelViewSet
from rest_framework import authentication

from .serializers import PostSerializer, PostDetailSerializer
from .models import Post
from .permissions import AuthorOrReadOnly


class PostViewSet(ModelViewSet):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [AuthorOrReadOnly]


    def get_serializer_class(self):
        if self.action == 'list':
            return PostSerializer
        return PostDetailSerializer
