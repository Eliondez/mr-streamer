from datetime import datetime
from django.db import models
from decimal import Decimal


class MarketData(models.Model):
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    prefix_id = models.PositiveIntegerField(verbose_name='Префикс', help_text='Например, 730 из ссылки')
    name = models.CharField(max_length=300, verbose_name='Идентификатор товара', help_text='Например "Glove Case"')
    json_data = models.JSONField(verbose_name='Данные по товару', blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.prefix_id, self.name)

    def save(self, *args, **kwargs):
        if not isinstance(self.json_data, list):
            return super(MarketData, self).save(*args, **kwargs)

        res = super(MarketData, self).save(*args, **kwargs)

        self.records.all().delete()
        for item in self.json_data:
            datetime_object = datetime.strptime(item[0], '%b %d %Y %H: +0')
            MarkerDataRecord.objects.create(
                market_data=self,
                timestamp=datetime_object,
                price=item[1],
                count=Decimal(item[2])
            )
        return res

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
        print('instance', instance)
        print('created', created)
        return instance, created

    class Meta:
        verbose_name = 'Данные по товару'
        verbose_name_plural = 'Товары'


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