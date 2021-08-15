import json

from datetime import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from marketdata.models import MarketData, MarkerDataRecord


class Command(BaseCommand):
    def handle(self, *args, **options):

        with open('items.json', 'r', encoding='UTF-8') as input_file:
            data = input_file.read()
            items = json.loads(data)
            for item_name, item_data in items.items():
                md, created = MarketData.objects.get_or_create(
                    name=item_name,
                    prefix_id=730
                )
                md.records.all().delete()
                records = []
                for item in item_data:
                    datetime_object = datetime.strptime(item[0], '%b %d %Y %H: +0')
                    records.append(MarkerDataRecord(
                        market_data=md,
                        timestamp=datetime_object,
                        price=item[1],
                        count=Decimal(item[2])
                    ))
                MarkerDataRecord.objects.bulk_create(records)
