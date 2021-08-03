from django.urls import path, include
from rest_framework import routers
from .viewsets import MarketDataViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'market_data', MarketDataViewSet)


urlpatterns = [
    path('', include(router.urls)),
]