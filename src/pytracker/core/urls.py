from django.urls import path, include, re_path
from .views import (
    home,
    UserHomeView,
    ProjectListView,
    ProjectCreateView,
    ProjectDetailView,
    ProjectUpdateView,
    ProjectDeleteView,
    TaskCreateView,
    TaskUpdateView,
    TaskDetailView,
    TaskDeleteView,
    CommentCreateView,
    DevelopersView,
    DevelopersAjaxDeleteView,
    TimeJournalView,
)

urlpatterns = [
    path(
        '',
        home,
        name='home'
    ),
    path(
        'users/<username>/',
        UserHomeView.as_view(),
        name="user_home"),
    path(
        'projects/',
        ProjectListView.as_view(),
        name='projects'
    ),
    path(
        'projects/add/',
        ProjectCreateView.as_view(),
        name='create_project'),
    path(
        'users/<username>/<slug:slug>/',
        ProjectDetailView.as_view(),
        name='project_detail'),
    path(
        'users/<username>/<slug:slug>/edit/',
        ProjectUpdateView.as_view(),
        name='project_edit'),
    path(
        'users/<username>/<slug:slug>/delete/',
        ProjectDeleteView.as_view(),
        name='project_delete'),
    path(
        'users/<username>/<slug:slug>/tasks/add/',
        TaskCreateView.as_view(),
        name='create_task'),
    path(
        'users/<username>/<slug:slug>/tasks/<int:pk>/detail/',
        TaskDetailView.as_view(),
        name='detail_task'),
    path(
        'users/<username>/<slug:slug>/tasks/<int:pk>/delete/',
        TaskDeleteView.as_view(),
        name='delete_task'),
    path(
        'users/<username>/<slug:slug>/tasks/<int:pk>/edit/',
        TaskUpdateView.as_view(),
        name='edit_task'),
    path(
        'users/<username>/<slug:slug>/tasks/<int:pk>/comments/add/',
        CommentCreateView.as_view(),
        name='add_comment'),
    path(
        'users/<username>/<slug:slug>/tasks/<int:pk>/time/',
        TimeJournalView.as_view(),
        name='time_journal'),
    path(
        'users/<username>/<slug:slug>/add/developers/',
        DevelopersView.as_view(),
        name='add_developer_in_project'),
    path(
        'users/<username>/<slug:slug>/delete/developers/<int:pk>',
        DevelopersAjaxDeleteView.as_view(),
        name='delete_developer_from_project'),
]
