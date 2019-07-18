""" This module include models definition for Comment. """

from django.db import models


class Comment(models.Model):
    """Model definition for Comment."""

    class Meta:
        """Meta definition for Comment."""

        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    comment = models.TextField()

    owner = models.ForeignKey(
        'user.UserProfile',
        null=True,
        on_delete=models.CASCADE
    )

    date_of_add = models.DateTimeField(
        "Date of adding",
        auto_now_add=True
    )

    for_task = models.ForeignKey(
        'core.Task',
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        """Unicode representation of Comment."""
        return "%s-%s" % (self.owner, self.date_of_add)
