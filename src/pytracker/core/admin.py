from django.contrib import admin
from .models import (Project,
                     Task,
                     Comment,
                     DeveloperInProject,
                     TimeJournal)


class CommentInline(admin.TabularInline):
    """ Config Comment inline display in Tasks. """

    model = Comment
    fields = ('owner', 'comment', 'date_of_add')
    readonly_fields = ('owner', 'comment', 'date_of_add')
    can_delete = False
    extra = 0

class DeveloperInProjectInline(admin.TabularInline):
    """ Config Developers inline display in Project. """

    model = DeveloperInProject
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
        DeveloperInProjectInline,
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
             'priority'
             )
         }
        ),
        ("Relations",
         {'fields': (
             'project',
             'creator',
             'performer'
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
    inlines = [
        CommentInline,
    ]


# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment)
admin.site.register(DeveloperInProject)
admin.site.register(TimeJournal)
