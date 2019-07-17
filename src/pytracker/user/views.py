from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import (CreateView,
                                       UpdateView)

from .models import UserProfile, UserGroup
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

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

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
