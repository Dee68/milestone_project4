# Generated by Django 3.2.18 on 2023-03-07 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_table_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='slug',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='table',
            name='title',
            field=models.CharField(default='restaurant table', max_length=100),
        ),
    ]
