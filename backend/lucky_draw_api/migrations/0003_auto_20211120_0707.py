# Generated by Django 3.2.9 on 2021-11-20 07:07

from django.db import migrations, models
import lucky_draw_api.models


class Migration(migrations.Migration):

    dependencies = [
        ('lucky_draw_api', '0002_auto_20211119_2344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='title',
        ),
        migrations.AddField(
            model_name='ticket',
            name='unique_code',
            field=models.CharField(blank=True, default=lucky_draw_api.models.generate_code, max_length=10),
        ),
    ]
