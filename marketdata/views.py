from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import MarkerDataRecord, MarketData


@csrf_exempt
def plain_post_view(request):
    post_data = json.loads(request.body)
    instance, created = MarketData.create_by_data(post_data)
    return HttpResponse()


def market_data_search_view(request):
    name = request.GET.get('name', '')
    if len(name) < 3:
        return HttpResponse('Пример поиска ?name=knife. Минимум три символа.')
    qs = MarkerDataRecord.objects.filter(market_data__name__icontains=name)\
        .values_list('market_data__name', 'timestamp', 'price', 'count')

    res = ''
    for i in qs:
        row = ','.join([i[0], i[1].strftime('%Y-%m-%d'), str(i[2]), str(i[3])]) + '\n'
        res += row

    return HttpResponse(res)
