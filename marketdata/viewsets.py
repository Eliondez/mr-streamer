from rest_framework import response, views, status, viewsets
from .models import MarketData
from .serializers import MarketDataSerializer


class MarketDataViewSet(viewsets.ViewSet):
    serializer_class = MarketDataSerializer

    def list(self, request):
        queryset = MarketData.objects.all()
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
