from django.urls import path
from django.conf.urls import include
from .viewsets import MarketDataViewSet, MarketDataLiteViewSet
from .views import plain_post_view, market_data_search_view, GetChartDataByIdsView, test_view

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'items', MarketDataViewSet, basename='market-items')
router.register(r'search_items', MarketDataLiteViewSet, basename='market-lite-items')
urlpatterns = router.urls


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'plain_upload/', plain_post_view),
    path(r'test/', test_view),
    path(r'market_data_search/', market_data_search_view),
    path(r'get_chart_data_by_ids/', GetChartDataByIdsView.as_view()),
]
