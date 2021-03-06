# Generated by Django 3.2.6 on 2021-08-07 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketdata', '0003_auto_20210807_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarkerDataRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(verbose_name='Дата-время сделки')),
                ('price', models.DecimalField(decimal_places=3, max_digits=12, verbose_name='Цена на день')),
                ('market_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketdata.marketdata', verbose_name='Товар в магазине')),
            ],
            options={
                'verbose_name': 'Сделка',
                'verbose_name_plural': 'Сделки по товарам',
            },
        ),
    ]
