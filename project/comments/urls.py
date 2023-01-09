from django.urls import path

from comments import views

app_name = 'comment'

urlpatterns = [
    path('posts/<post_id>/add-comment', views.AddCommentAPIView.as_view(), name='add-comment'),
    path('posts/<post_id>/comment/<comment_id>/', views.AddCommentAPIView.as_view(), name='update-comment'),
    path('posts/<post_id>/comment/<comment_id>', views.AddCommentAPIView.as_view(), name='delete-comment'),
]
