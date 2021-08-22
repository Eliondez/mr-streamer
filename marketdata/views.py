from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
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


class GetChartDataByIdsView(APIView):

    def get(self, request):
        res = Response([])
        ids_string = request.GET.get('ids')
        if not ids_string:
            return res
        ids = [int(md_id) for md_id in ids_string.split(',') if md_id]
        md_records = MarkerDataRecord.objects.filter(market_data_id__in=ids).order_by('timestamp')
        min_date_by_md_id = dict()
        deltas_by_delta = dict()

        md_ids = set()

        for i in md_records:
            md_ids.add(i.market_data_id)
            if i.market_data_id not in min_date_by_md_id:
                min_date_by_md_id[i.market_data_id] = i.timestamp
            delta = (i.timestamp - min_date_by_md_id[i.market_data_id]).days + 1
            if delta not in deltas_by_delta:
                deltas_by_delta[delta] = {
                    'day': delta
                }
            deltas_by_delta[delta]['id{}'.format(i.market_data_id)] = i.price
        market_items = MarketData.objects.filter(id__in=md_ids)
        series = [{'valueField': 'id{}'.format(i.id), 'name': i.name} for i in market_items]
        return Response({
            'data': deltas_by_delta.values(),
            'series':  series
        })
