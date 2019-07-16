from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from .models import Task
from django.template.loader import get_template
from django.template.loader import render_to_string


# Create your task here

@shared_task
def task_update_notification(changes, creator_email):
    """Task Update Notification"""

    topic = Task.objects.get(pk=changes['pk']).topic

    recipient_list = [creator_email,]
    if 'performer' in changes['old'].keys():
        recipient_list.append(changes['old']['performer'])
        recipient_list.append(changes['new']['performer'])
    else:
        recipient_list.append(Task.objects.get(pk=changes['pk']).performer.user.email)

    body = render_to_string('email/email.html', context={'old': changes['old'], 'new': changes['new'], 'topic':topic})

    email = EmailMultiAlternatives(
        subject='Task - {0} is update.'.format(topic),
        body=body,
        to=recipient_list
    )
    email.send(fail_silently=False)
