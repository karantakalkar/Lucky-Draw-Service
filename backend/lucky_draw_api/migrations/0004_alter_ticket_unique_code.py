# Generated by Django 3.2.9 on 2021-11-20 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lucky_draw_api', '0003_auto_20211120_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='unique_code',
            field=models.CharField(max_length=10),
        ),
    ]
