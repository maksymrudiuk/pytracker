from django.db import models
from django.template.defaultfilters import slugify
from tinymce import models as tinymce_models

# Create your models here.
class Project(models.Model):
    """ Model definition for Project. """

    class Meta:
        """ Meta definition for Project. """

        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-created_at']

    slug_id = models.SlugField(
        "Unique string id",
        max_length=255,
        unique=True,
        editable=False,
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
        through='Developer')

    description = tinymce_models.HTMLField(
        "Desrciption"
    )

    created_at = models.DateTimeField(
        "Created at",
        auto_now_add=True
    )

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        super(Project, self).save(*args, **kwargs)
        if not self.slug_id:
            self.slug_id = slugify(self.name) + '-' + str(self.id)
            self.save()

    def __str__(self):
        """Unicode representation of Project."""
        return "%s" % self.name


class Developer(models.Model):
    """Model definition for Developer."""

    class Meta:
        """Meta definition for Developer."""

        verbose_name = 'Developer'
        verbose_name_plural = 'Developers'
        ordering = ['-id']

    user = models.ForeignKey(
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
        """Unicode representation of Developer."""
        return "%s - %s" % (self.user, self.project.name)
