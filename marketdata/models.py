import json
from datetime import datetime
from django.db import models
from decimal import Decimal


class MarketData(models.Model):
    DATE_FORMAT = '%b %d %Y %H: +0'

    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    prefix_id = models.PositiveIntegerField(verbose_name='Префикс', help_text='Например, 730 из ссылки')
    name = models.CharField(max_length=300, verbose_name='Идентификатор товара', help_text='Например "Glove Case"')
    json_data = models.JSONField(verbose_name='Данные по товару', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(verbose_name='Рейтинг', default=50)
    last_loaded = models.DateTimeField(verbose_name='Дата последнего обновления информации', default=datetime.now)
    last_data_expanded = models.DateTimeField(verbose_name='Дата последней информации', default=datetime.now)
    last_meta_calculated = models.DateTimeField(verbose_name='Дата последней пересчёта мета-информации',
                                                default=datetime.now)
    preview_data = models.JSONField(null=True, blank=True, verbose_name='До 10 точек для превью')
    date_start_trade = models.DateField(null=True, blank=True, verbose_name='Дата начала торгов')

    def __str__(self):
        return '{} {}'.format(self.prefix_id, self.name)

    def save(self, *args, **kwargs):
        res = super(MarketData, self).save(*args, **kwargs)
        return res

    def create_sub_items(self):
        data = self.get_items_from_json_data()
        real_records_count = self.records.count()
        if len(data) == real_records_count:
            return
        print('need update', self.id)
        items = []
        self.records.all().delete()
        for data_item in data:
            datetime_object = datetime.strptime(data_item[0], self.DATE_FORMAT)
            items.append(MarkerDataRecord(
                market_data=self,
                timestamp=datetime_object,
                price=data_item[1],
                count=Decimal(data_item[2])
            ))
        MarkerDataRecord.objects.bulk_create(items)

    def get_items_from_json_data(self):
        if isinstance(self.json_data, str):
            data = json.loads(self.json_data)
        elif isinstance(self.json_data, list):
            data = self.json_data
        else:
            data = []
        return data

    @classmethod
    def create_by_data(cls, data):
        instance, created = cls.objects.get_or_create(
            name=data.get('name'),
            prefix_id=data.get('prefix_id'),
            defaults={'json_data': data.get('json_data')}
        )
        if not created:
            instance.json_data = data.get('json_data')
            instance.save()
        return instance, created

    class Meta:
        verbose_name = 'Данные по товару'
        verbose_name_plural = 'Товары'
        ordering = ('id',)


class MarkerDataRecord(models.Model):
    market_data = models.ForeignKey('MarketData', verbose_name='Товар в магазине',
                                    related_name='records', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(verbose_name='Дата-время сделки')
    price = models.DecimalField(max_digits=12, decimal_places=3, verbose_name='Цена', default=0)
    count = models.DecimalField(max_digits=12, decimal_places=3, verbose_name='Количество', default=0)

    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки по товарам'

    @property
    def name(self):
        return self.market_data.name