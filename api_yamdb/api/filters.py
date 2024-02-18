import django_filters

from reviews.models import Title


class TitleFilterSet(django_filters.FilterSet):
    """Фильтр по полям произведений."""
    name = django_filters.CharFilter(lookup_expr='icontains')
    year = django_filters.NumberFilter(lookup_expr='icontains')
    genre = django_filters.CharFilter(field_name='genre__slug',
                                      lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__slug',
                                         lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['name', 'genre', 'category', 'year']
