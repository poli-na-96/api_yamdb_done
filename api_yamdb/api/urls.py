from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (token, signup, ReviewsViewSet, CommentsViewSet, GenreViewSet,
                    TitleViewSet, CategoryViewSet)

app_name = 'api'
router = DefaultRouter()


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', token, name='token'),
    path('v1/auth/signup/', signup, name='token'),
#    path('v1/users/me/', UserView.as_view(), name='user_me'),

router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewsViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments'
)
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(router.urls)),
]
