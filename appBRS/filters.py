from .models import Bike
import django_filters


class bike_filter(django_filters.FilterSet):
    class Meta():
        model = Bike
        fields = ['bike_number', 'bike_color',
                  'bike_type', 'bike_model', 'bike_brand', 'bike_station']
