from django.db import models
from django.template.defaultfilters import slugify
from tinymce import models as tinymce_models

# Create your models here.
class Project(models.Model):
    """Model definition for Project."""

    class Meta:
        """Meta definition for Project."""

        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    slug_id = models.SlugField(
        "Unique string id",
        max_length=255,
        unique=True,
        blank=True
    )

    name = models.CharField(
        "Name",
        max_length=200,
        blank=False
    )

    owner = models.ForeignKey(
        'user.UserProfile',
        related_name='project_owner',
        null=True,
        on_delete=models.CASCADE
    )

    developers = models.ManyToManyField(
        'user.UserProfile',
        through='DeveloperInProject')

    description = tinymce_models.HTMLField(
        "Desrciption"
    )

    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)
        if not self.slug_id:
            self.slug_id = slugify(self.name) + '-' + str(self.id)
            self.save()

    def __str__(self):
        """Unicode representation of Project."""
        return "%s" % self.name


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

    topic = models.CharField(
        "Topic",
        max_length=255,
        blank=False
    )

    description = tinymce_models.HTMLField(
        "Desrciption"
    )

    start_date = models.DateTimeField()

    end_date = models.DateTimeField()

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

    estimated_time = models.SmallIntegerField()

    creator = models.ForeignKey(
        'user.UserProfile',
        related_name='user_creator',
        null=True,
        on_delete=models.CASCADE
    )

    performer = models.ForeignKey(
        'user.UserProfile',
        related_name='user_performer',
        null=True,
        on_delete=models.SET_NULL
    )

    project = models.ForeignKey(
        'core.Project',
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        """Unicode representation of Task."""
        return "%s" % self.topic


class Comment(models.Model):
    """Model definition for Comment."""

    # TODO: Define fields here

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


class DeveloperInProject(models.Model):
    """Model definition for DeveloperInProject."""


    class Meta:
        """Meta definition for DeveloperInProject."""

        verbose_name = 'Developer In Project'
        verbose_name_plural = 'Developer In Projects'

    developer = models.ForeignKey(
        'user.UserProfile',
        null=True,
        on_delete=models.SET_NULL
    )

    project = models.ForeignKey(
        'core.Project',
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        """Unicode representation of DeveloperInProject."""
        return "%s - %s" % (self.developer, self.project.name)


class TimeLogging(models.Model):
    """Model definition for TimeLogging."""


    class Meta:
        """Meta definition for TimeLogging."""

        verbose_name = 'TimeLogging'
        verbose_name_plural = 'TimeLoggings'

    spent_time = models.SmallIntegerField()

    notes = models.TextField()

    task = models.ForeignKey(
        'core.Task',
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        """Unicode representation of TimeLogging."""
        return "%s" % (self.task)
