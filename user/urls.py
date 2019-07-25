""" URLs config for user app. """

from django.urls import path
from .views import (
    SignUpView,
    UpdateUserProfileView,
    UserProfileDetailView)

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('<int:pk>/update', UpdateUserProfileView.as_view(), name='update_user'),
    path('profile/<str:username>', UserProfileDetailView.as_view(), name='user_profile')
]
