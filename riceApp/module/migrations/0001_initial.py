# Generated by Django 4.2.13 on 2024-05-23 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PopulationData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('population', models.FloatField()),
                ('consumptionRate', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='StockRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataType', models.BooleanField()),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('avgStock', models.FloatField()),
            ],
        ),
    ]
