from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import (GenreViewSet,
                    TitleViewSet, CategoryViewSet)

router = DefaultRouter()
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('v1/', include(router.urls)),
]
