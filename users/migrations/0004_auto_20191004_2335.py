# Generated by Django 2.2.2 on 2019-10-04 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20191004_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='country',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='customuser',
            name='state',
            field=models.CharField(default='', max_length=200),
        ),
    ]
