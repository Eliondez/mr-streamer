from django.db.models import Count

from rest_framework import response, status, viewsets
from rest_framework import filters, pagination, mixins
from .models import MarketData
from marketdata import serializers as md_serializers


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 500


class MarketDataViewSet(viewsets.ViewSet):
    serializer_class = md_serializers.MarketDataFullSerializer
    pagination_class = pagination.PageNumberPagination

    def list(self, request):
        queryset = MarketData.objects.all()[:100]
        serializer_class = self.serializer_class
        return response.Response(serializer_class(queryset, many=True).data)

    def create(self, request):
        serializer_class = self.serializer_class
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        prefix_id = serializer.validated_data.get('prefix_id')
        name = serializer.validated_data.get('name')
        json_data = serializer.validated_data.get('json_data')

        instance, created = MarketData.objects.get_or_create(
            name=name,
            prefix_id=prefix_id,
            defaults={'json_data': json_data}
        )
        if not created:
            instance.json_data = json_data
            instance.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class MarketDataLiteViewSet(mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = md_serializers.MarketDataLiteSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )

    def get_serializer_class(self):
        return {
            'update': md_serializers.MarketDataUpdateSerializer
        }.get(self.action, self.serializer_class)

    def get_queryset(self):
        # return MarketData.objects.all().order_by('id').filter(id__lte=2200).exclude(name__icontains='key')
        return MarketData.objects.exclude(name__istartswith='★').order_by('id')
