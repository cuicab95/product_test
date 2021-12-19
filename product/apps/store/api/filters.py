from django_filters import rest_framework as filters
from ..models import Order


class OrderFilter(filters.FilterSet):

    class Meta:
        model = Order
        fields = {
            'id':  ['exact'],
            'is_urgent':  ['exact'],
            'type': ['exact'],
            'customer__type': ['exact'],
            'assortment_date': ['exact', 'isnull'],
        }
