from django.db import models
from tinymce import models as tinymce_models

# Create your models here.
class Project(models.Model):
    """Model definition for Project."""

    class Meta:
        """Meta definition for Project."""

        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    slug_id = models.SlugField(
        "Unique string id"
    )

    name = models.CharField(
        "Name",
        max_length=200,
        blank=False
    )

    description = tinymce_models.HTMLField(
        "Desrciption"
    )

    def __str__(self):
        """Unicode representation of Project."""
        return self.name

