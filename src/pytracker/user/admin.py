from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, UserGroup


# Register your models here.
class UsersInline(admin.TabularInline):
    """ Config user inline display. """

    model = UserProfile
    fields = ('first_name', 'last_name', 'position', 'username')
    extra = 0


class UserProfileAdmin(UserAdmin):
    """ Config and group fields in UserProfile model. """

    fieldsets = (
        ("General",
         {'fields': (
             'username',
             'email',
             'password'
             )
         }
        ),
        ("Personal",
         {'fields': (
             'first_name',
             'last_name',
             'date_of_birth',
             'position',
             'photo'
             )
         }
        ),
        ("Permissions",
         {'fields': (
             'is_active',
             'is_staff',
             'is_superuser',
             'groups',
             )
         }
        ),
        ("Important dates",
         {'fields': (
             'last_login',
             'date_joined'
             )
         }
        ),
    )


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserGroup)
