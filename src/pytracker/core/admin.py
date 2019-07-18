""" Admin settings for core app and reletive Models. """

from django.contrib import admin
from .models import (Project,
                     Task,
                     Comment,
                     Developer,
                     TimeJournal)


class CommentInline(admin.TabularInline):
    """ Config Comment inline display in Tasks. """

    model = Comment
    fields = ('owner', 'comment', 'date_of_add')
    readonly_fields = ('owner', 'comment', 'date_of_add')
    can_delete = False
    extra = 0

class DevelopersInline(admin.TabularInline):
    """ Config Developers inline display in Project. """

    model = Developer
    verbose_name = "Developer"
    verbose_name_plural = "Developers"
    can_delete = False
    extra = 0

class TaskInline(admin.TabularInline):
    """ Config Tasks inline display in Project. """

    model = Task
    fields = ('topic', 'priority', 'start_date', 'end_date', 'estimated_time')
    readonly_fields = ('topic', 'priority', 'start_date', 'end_date', 'estimated_time')
    can_delete = False
    extra = 0

class ProjectAdmin(admin.ModelAdmin):
    """ Config Projects display. """

    inlines = [
        DevelopersInline,
        TaskInline,
    ]

class TaskAdmin(admin.ModelAdmin):
    """ Config Projects display. """

    fieldsets = (
        ("General",
         {'fields': (
             'topic',
             'description',
             'task_type',
             'priority',
             'status'
             )
         }
        ),
        ("Relations",
         {'fields': (
             'creator',
             'project',
             'performer',
             )
         }
        ),
        ("Time Managment",
         {'fields': (
             'start_date',
             'end_date',
             'estimated_time'
             )
         }
        )
    )

    readonly_fields = ('creator', 'status',)

    inlines = [
        CommentInline,
    ]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'creator', None) is None:
            obj.creator = request.user
        if getattr(obj, 'performer', None) is None:
            obj.status = 1
        if getattr(obj, 'performer', None) is not None:
            obj.status = 2
        obj.save()


# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment)
admin.site.register(Developer)
admin.site.register(TimeJournal)
