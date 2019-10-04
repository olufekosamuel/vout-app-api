# Generated by Django 2.2.2 on 2019-10-04 00:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_channelcomplain'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelComplainComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('Complain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.ChannelComplain')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.ChannelUsers')),
            ],
        ),
    ]
