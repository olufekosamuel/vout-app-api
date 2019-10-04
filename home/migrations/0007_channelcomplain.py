# Generated by Django 2.2.2 on 2019-10-04 00:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_remove_channel_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelComplain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('is_verified', models.BooleanField(default=False)),
                ('is_irrelevant', models.BooleanField(default=False)),
                ('is_solved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('Channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Channel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.ChannelUsers')),
            ],
        ),
    ]
