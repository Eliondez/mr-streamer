from django.contrib import admin
from django.urls import path, include
from .views import index_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/market-data/', include('marketdata.urls')),
    path('', index_view)
]
