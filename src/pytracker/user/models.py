from django.db import models
from django.contrib.auth.models import AbstractUser, Group

# Create your models here.
class UserProfile(AbstractUser):
    """ Model definition for UserProfile. """

    class Meta:
        """ Meta definition for UserProfile. """

        verbose_name = "User"
        verbose_name_plural = "Users"

    POSITIONS = (
        (1, 'Admin'),
        (2, 'Developer'),
    )

    first_name = models.CharField(
        "First name",
        max_length=100,
        blank=False
    )

    last_name = models.CharField(
        "Last name",
        max_length=100,
        blank=False
    )

    date_of_birth = models.DateField(
        "Date of birth",
        null=True
    )

    position = models.SmallIntegerField(
        "Position",
        choices=POSITIONS,
        null=True,
        blank=False
    )

    photo = models.ImageField(
        "User photo",
        blank=True
    )

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.get_short_name()

    @property
    def is_admin(self):
        """ Check user role. """
        return self.position == 1

    @property
    def is_developer(self):
        """ Check user role. """
        return self.position == 2


class UserGroup(Group):
    class Meta:
        proxy = True
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'