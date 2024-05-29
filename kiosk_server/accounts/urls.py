from django.urls import path
from django.conf.urls import include
from .views import CustomUserDetailView, MembershipView

urlpatterns = [
    path('', CustomUserDetailView.as_view(), name='user-detail'),
    path('membership/', MembershipView.as_view(), name='membership'),
    path('membership/<int:membership_ID>/', MembershipView.as_view(), name='membership-detail'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
]
