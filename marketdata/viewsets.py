from rest_framework import viewsets
from .models import MarketData
from .serializers import MarketDataSerializer


class MarketDataViewSet(viewsets.ModelViewSet):
    queryset = MarketData.objects.all()
    serializer_class = MarketDataSerializer