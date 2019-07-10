from django.contrib import admin
from .models import Project, Task, Comment, DeveloperInProject, TimeLogging


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ('owner', 'comment', 'date_of_add')
    readonly_fields = ('owner', 'comment', 'date_of_add')
    can_delete = False
    extra = 0

class DeveloperInProjectInline(admin.TabularInline):
    model = DeveloperInProject
    verbose_name = "Developer"
    verbose_name_plural = "Developers"
    can_delete = False
    extra = 0

class TaskInline(admin.TabularInline):
    model = Task
    fields = ('topic', 'priority', 'start_date', 'end_date', 'estimated_time')
    readonly_fields = ('topic', 'priority', 'start_date', 'end_date', 'estimated_time')
    can_delete = False
    extra = 0

class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        DeveloperInProjectInline,
        TaskInline,
    ]

class TaskAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]


# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment)
admin.site.register(TimeLogging)
