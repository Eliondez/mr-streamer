from rest_framework import serializers
from .models import MarketData


class MarketDataFullSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MarketData
        fields = ['updated', 'prefix_id', 'name']


class MarketDataUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketData
        fields = ['id', 'rating']


class MarketDataLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketData
        fields = ['id', 'name', 'prefix_id', 'rating']
