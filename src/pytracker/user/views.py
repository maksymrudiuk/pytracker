from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView

from .models import UserProfile
from .forms import (BaseSignUpUserProfileForm,
                    UpdateUserProfileForm)


# Create your views here.
class SignUpView(CreateView):
    model = UserProfile
    form_class = BaseSignUpUserProfileForm
    template_name = 'user/form.html'

    def get_success_url(self):
        return reverse('update-user', kwargs={'pk': self.object.pk})


class UpdateUserProfileView(UpdateView):
    model = UserProfile
    form_class = UpdateUserProfileForm
    template_name = 'user/form.html'

    def get_success_url(self):
        return reverse('home')
