from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/doc/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-doc'),

    # project app urls
    path('api/user/', include('blog_users.urls')),

]
