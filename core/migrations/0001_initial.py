# Generated by Django 2.2.3 on 2019-07-10 12:58

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug_id', models.SlugField()),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', tinymce.models.HTMLField()),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
    ]