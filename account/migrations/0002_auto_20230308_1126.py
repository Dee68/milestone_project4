# Generated by Django 3.2.18 on 2023-03-08 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.CharField(default='first name', max_length=15),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(default='last name', max_length=15),
        ),
    ]