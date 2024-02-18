from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (token, signup, ReviewsViewSet, CommentsViewSet,
                    GenreViewSet, TitleViewSet, CategoryViewSet,
                    UserViewSet)

app_name = 'api'
router = DefaultRouter()

router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewsViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments'
)
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'users', UserViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', token, name='token'),
    path('v1/auth/signup/', signup, name='signup'),
]
