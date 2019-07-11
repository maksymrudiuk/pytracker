from django.urls import path
from . import views

urlpatterns = [
    # path('', views.test, name="home"),
    path('', views.HomeView.as_view(), name="home"),
    path('project/add/', views.ProjectsCreateView.as_view(), name='create_project'),
    path('project/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
]