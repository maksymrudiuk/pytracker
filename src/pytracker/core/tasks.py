""" Celery tasks for core app. """

from __future__ import absolute_import, unicode_literals
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from celery import shared_task
from .models import Task


# Create your task here

@shared_task
def task_update_notification(changes, creator_email):
    """Task Update Notification"""

    topic = Task.objects.get(pk=changes['pk']).topic

    recipient_list = [creator_email,]

    if 'perfomer' in changes['old'].keys():
        if changes['old']['performer'] is None:
            recipient_list.append(changes['new']['performer'])
        elif changes['new']['performer'] is None:
            recipient_list.append(changes['old']['performer'])
        else:
            recipient_list.append(changes['new']['performer'])
            recipient_list.append(changes['old']['performer'])
    else:
        performer = Task.objects.get(pk=changes['pk']).performer
        if performer is not None:
            recipient_list.append(performer.user.email)


    body = render_to_string('email/email.html', context={
        'old': changes['old'],
        'new': changes['new'],
        'topic':topic})

    email = EmailMultiAlternatives(
        subject='Task - {0} is update.'.format(topic),
        body=body,
        to=recipient_list
    )
    email.send(fail_silently=False)
