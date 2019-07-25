from django.db import models


class TimeJournal(models.Model):
    """Model definition for TimeJournal."""

    class Meta:
        """Meta definition for TimeJournal."""

        verbose_name = 'TimeJournal'
        verbose_name_plural = 'TimeJournals'

    spent_time = models.DecimalField(max_digits=5, decimal_places=2)

    notes = models.TextField()

    owner = models.ForeignKey(
        'user.UserProfile',
        null=True,
        default=None,
        on_delete=models.CASCADE
    )

    task = models.ForeignKey(
        'core.Task',
        null=True,
        default=None,
        on_delete=models.CASCADE
    )

    def __str__(self):
        """Unicode representation of TimeJournal."""
        return "%s - %s" % (self.task, self.spent_time)
