from rest_framework import filters
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet

from .permissions import AdminOrReadOnly


class GetListCreateDeleteMixin(GenericViewSet, CreateModelMixin,
                               ListModelMixin, DestroyModelMixin):
    permission_classes = [AdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
