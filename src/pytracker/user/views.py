from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import (CreateView,
                                       UpdateView)

from .models import UserProfile
from .forms import (BaseSignUpUserProfileForm,
                    UpdateUserProfileForm)


# Create your views here.
class SignUpView(CreateView):
    """ Sign up User View Definition. """

    model = UserProfile
    form_class = BaseSignUpUserProfileForm
    template_name = 'user/form.html'

    def get_success_url(self):
        return reverse('update-user', kwargs={'pk': self.object.pk})


class UpdateUserProfileView(UpdateView):
    """ Update User View Definition. """

    model = UserProfile
    form_class = UpdateUserProfileForm
    template_name = 'user/form.html'

    def get_success_url(self):
        return reverse('home')
