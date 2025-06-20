# Generated by Django 5.0.6 on 2025-03-03 07:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Properties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.TextField()),
                ('type', models.CharField(max_length=30)),
                ('location', models.CharField(max_length=1000)),
                ('status', models.CharField(max_length=30)),
                ('area', models.CharField(max_length=30)),
                ('beds', models.IntegerField()),
                ('baths', models.IntegerField()),
                ('price', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='ppt_image')),
                ('video', models.ImageField(blank=True, null=True, upload_to='ppt_video')),
                ('agent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
