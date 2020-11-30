from django_filters import FilterSet, DateFilter, CharFilter
from .models import *


class OrderFilter(FilterSet):
    start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')
    note = CharFilter(field_name='note', lookup_expr='icontains')

    class Meta:
        model = Order
        fields = ['product', 'status', 'note', 'date_created']
        # Eu poderia não ter adicionado o 'date_created' acima, mas coloquei para testar o exclude command
        exclude = ['date_created']
