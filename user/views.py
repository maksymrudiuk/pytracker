""" This module include Views definition for User model """
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import (
    CreateView,
    UpdateView)
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import UserProfile, UserGroup
from .forms import (
    BaseSignUpUserProfileForm,
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

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()  # pylint: disable=attribute-defined-outside-init

        if self.object.position == 1:
            self.object.groups.add(UserGroup.objects.get(name='admins'))
        if self.object.position == 2:
            self.object.groups.add(UserGroup.objects.get(name='developers'))

        self.object.save()

        return super(UpdateUserProfileView, self).post(
            request,
            *args,
            **kwargs
        )



class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = "user/user_profile.html"
    context_object_name = 'profile'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserProfileDetailView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(UserProfile, username=self.kwargs.get('username'))
