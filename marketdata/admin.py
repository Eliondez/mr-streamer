from django.contrib import admin
from .models import MarketData, MarkerDataRecord


class MarketDataRecord(admin.TabularInline):
    model = MarkerDataRecord
    extra = 0


class MarketDataAdmin(admin.ModelAdmin):
    inlines = [MarketDataRecord, ]


admin.site.register(MarketData, MarketDataAdmin)
