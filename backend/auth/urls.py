from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from auth.views import MyObtainTokenPairView, RegisterView


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='retrieve_tokens_pairs'),
    path('login/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('register/', RegisterView.as_view(), name='register_user'),
]
