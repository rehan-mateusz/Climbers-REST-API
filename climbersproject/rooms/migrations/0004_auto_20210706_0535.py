# Generated by Django 3.2.3 on 2021-07-06 05:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rooms', '0003_auto_20210705_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acc_to_room', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='membership',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_to_acc', to='rooms.room'),
        ),
        migrations.AlterField(
            model_name='room',
            name='members',
            field=models.ManyToManyField(blank=True, through='rooms.Membership', to=settings.AUTH_USER_MODEL),
        ),
    ]