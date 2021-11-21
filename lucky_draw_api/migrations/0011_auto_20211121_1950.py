# Generated by Django 3.2.9 on 2021-11-21 19:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lucky_draw_api', '0010_alter_luckydraw_timing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='winner',
            name='name',
        ),
        migrations.AddField(
            model_name='ticket',
            name='used_at',
            field=models.CharField(default='N/A', max_length=100),
        ),
        migrations.AddField(
            model_name='winner',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='winner',
            name='win_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]