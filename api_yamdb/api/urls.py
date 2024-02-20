from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                    ReviewsViewSet, TitleViewSet, UserViewSet, signup, token)

app_name = 'api'
v1_router = DefaultRouter()

v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewsViewSet, basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments'
)
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('users', UserViewSet)


auth_patterns = [
    path('auth/token/', token, name='token'),
    path('auth/signup/', signup, name='signup'),
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include(auth_patterns)),
]
