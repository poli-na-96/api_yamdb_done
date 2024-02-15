from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import token, signup


v1_router = DefaultRouter()


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/', token, name='token'),
    path('v1/auth/signup/', signup, name='token'),
#    path('v1/users/me/', UserView.as_view(), name='user_me'),
]
