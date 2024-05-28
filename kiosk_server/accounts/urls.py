from django.urls import path
from django.conf.urls import include
from .views import CustomUserDetailView

urlpatterns = [
    path('', CustomUserDetailView.as_view(), name='user-detail'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
]
