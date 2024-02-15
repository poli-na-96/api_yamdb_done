from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ReviewsViewSet, CommentsViewSet, GenreViewSet,
                    TitleViewSet, CategoryViewSet)



app_name = 'api'

router = DefaultRouter()
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
