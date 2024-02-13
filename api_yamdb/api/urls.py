from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)

from .views import token, signup


v1_router = DefaultRouter()


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/', token, name='token'),
    path('v1/auth/signup/', signup, name='token'),
    path('v1/api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
