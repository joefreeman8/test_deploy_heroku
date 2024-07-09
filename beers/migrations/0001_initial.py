# Generated by Django 5.0.6 on 2024-07-02 12:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('breweries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
                ('style', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500)),
                ('abv', models.FloatField()),
                ('brewery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beers', to='breweries.brewery')),
            ],
        ),
    ]
