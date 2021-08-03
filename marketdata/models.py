from django.db import models


class MarketData(models.Model):
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    prefix_id = models.PositiveIntegerField(verbose_name='Префикс')
    name = models.CharField(max_length=300, verbose_name='Идентификатор товара')
    fake_data = models.TextField(verbose_name='Данные по товару (предварительно)')

    def __str__(self):
        return f'{self.prefix_id} {self.name}'
