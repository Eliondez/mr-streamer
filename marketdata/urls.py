from django.urls import path
from django.conf.urls import include
from .viewsets import MarketDataViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'items', MarketDataViewSet, basename='market-items')
urlpatterns = router.urls


urlpatterns = [
    path(r'', include(router.urls)),
]
