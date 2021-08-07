from rest_framework import serializers
from .models import MarketData


class MarketDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MarketData
        fields = ['updated', 'prefix_id', 'name', 'json_data']
