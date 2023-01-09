from django.db.models import Q

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

    def get_queryset(self):
        search = self.request.query_params.get('search', None)
        if search is not None:
            return self.queryset.filter(Q(title__icontains=search)|Q(body__icontains=search)).order_by('-created_at').distinct()
        return self.queryset
        
    def get_serializer_class(self):
        if self.action == 'list':
            return PostSerializer
        return PostDetailSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)