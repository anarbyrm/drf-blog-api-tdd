from django.urls import path

from .views import CreateUserAPIView, CreateAuthToken


app_name = 'user'

urlpatterns = [
    path('create/', CreateUserAPIView.as_view(), name='create'),
    path('token/', CreateAuthToken.as_view(), name='token'),
    
]
