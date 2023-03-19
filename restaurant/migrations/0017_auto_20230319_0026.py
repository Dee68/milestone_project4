# Generated by Django 3.2.18 on 2023-03-19 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0016_drink_food'),
    ]

    operations = [
        migrations.AddField(
            model_name='drink',
            name='drink_type',
            field=models.CharField(choices=[('wines', 'Wines'), ('beers', 'Beers'), ('cocktails', 'Cocktails')], default='wines', max_length=9),
        ),
        migrations.AddField(
            model_name='food',
            name='food_type',
            field=models.CharField(choices=[('snacks', 'Snacks'), ('main', 'Main'), ('desert', 'Desert')], default='snacks', max_length=7),
        ),
    ]
