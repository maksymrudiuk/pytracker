from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.HomeView.as_view(),
        name="home"),
    path(
        'project/add/',
        views.ProjectsCreateView.as_view(),
        name='create_project'),
    path(
        'project/<slug:slug>/',
        views.ProjectDetailView.as_view(),
        name='project_detail'),
    path(
        'project/<slug:slug>/task/add/',
        views.TaskCreateView.as_view(),
        name='create_task'),
    path(
        'project/<slug:slug>/task/<int:pk>/detail/',
        views.TaskDetailView.as_view(),
        name='detail_task'),
    path(
        'project/<slug:slug>/task/<int:pk>/delete/',
        views.TaskDeleteView.as_view(),
        name='delete_task'),
    path(
        'project/<slug:slug>/task/<int:pk>/edit/',
        views.TaskUpdateView.as_view(),
        name='edit_task'),
    path(
        'project/<slug:slug>/task/<int:pk>/comment/add/',
        views.CommentCreateView.as_view(),
        name='add_comment'),
    path(
        'project/<slug:slug>/add/developer/',
        views.DevelopersView.as_view(),
        name='add_developer_in_project')
]