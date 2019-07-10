# Generated by Django 2.2.3 on 2019-07-10 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=tinymce.models.HTMLField(verbose_name='Desrciption'),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug_id',
            field=models.SlugField(verbose_name='Unique string id'),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=255, verbose_name='Topic')),
                ('desciption', tinymce.models.HTMLField(verbose_name='Desrciption')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('task_type', models.SmallIntegerField(choices=[(1, 'Feature'), (2, 'Bug')], verbose_name='Task type')),
                ('priority', models.SmallIntegerField(choices=[(1, 'Normal'), (2, 'High'), (3, 'Urgently')], verbose_name='Priority')),
                ('estimated_time', models.SmallIntegerField()),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creator', to=settings.AUTH_USER_MODEL)),
                ('performer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_performer', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Project')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desciption', tinymce.models.HTMLField(verbose_name='Desrciption')),
                ('date_of_add', models.DateTimeField(auto_now_add=True, verbose_name='Date of adding')),
                ('for_task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Task')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Project')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
    ]
