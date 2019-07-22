""" URLs config for user app. """

from django.urls import path
from .views import SignUpView, UpdateUserProfileView

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('<int:pk>/update', UpdateUserProfileView.as_view(), name='update-user')
]
