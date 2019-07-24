""" This module include models definition for Task. """

from django.db import models
from tinymce import models as tinymce_models


class Task(models.Model):
    """Model definition for Task."""

    class Meta:
        """Meta definition for Task."""

        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    TASK_TYPES = (
        (1, 'Feature'),
        (2, 'Bug'),
    )

    TASK_PRIORITY = (
        (1, 'Normal'),
        (2, 'High'),
        (3, 'Urgently'),
    )

    TASK_STATUS = (
        (1, 'Free'),
        (2, 'Performing'),
        (3, 'Done')
    )

    topic = models.CharField(
        "Topic",
        max_length=255,
        blank=False
    )

    description = tinymce_models.HTMLField(
        "Desrciption"
    )

    start_date = models.DateTimeField(
        null=True
    )

    end_date = models.DateTimeField(
        null=True
    )

    task_type = models.SmallIntegerField(
        "Task type",
        choices=TASK_TYPES,
        blank=False
    )

    priority = models.SmallIntegerField(
        "Priority",
        choices=TASK_PRIORITY,
        blank=False
    )

    status = models.SmallIntegerField(
        'Status',
        choices=TASK_STATUS,
        blank=False,
        editable=False,
        default=1
    )

    estimated_time = models.DecimalField(max_digits=5, decimal_places=2)

    creator = models.ForeignKey(
        'user.UserProfile',
        related_name='user_creator',
        null=True,
        editable=False,
        on_delete=models.CASCADE
    )

    performer = models.ForeignKey(
        'user.UserProfile',
        related_name='user_performer',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    project = models.ForeignKey(
        'core.Project',
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        """Unicode representation of Task."""
        return "(%s - %s)" % (self.topic, self.creator)
