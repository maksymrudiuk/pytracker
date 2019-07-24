# Generated by Django 2.2.3 on 2019-07-24 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_timejournal_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timejournal',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]