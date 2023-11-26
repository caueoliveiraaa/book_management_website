import django_filters
from .models import Books


class BookFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Books
        fields = ('name', 'author')