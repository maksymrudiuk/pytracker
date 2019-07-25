""" This module include Views definition for User model """
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import (
    CreateView,
    UpdateView)
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
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
    template_name = 'user/form.html'

    def get(self, request, *args, **kwargs):

        context = {
            'form': BaseSignUpUserProfileForm,
            'title': 'Sign Up'
        }

        return render(request, 'user/form.html', context)

    def post(self, request, *args, **kwargs):

        form = BaseSignUpUserProfileForm(self.request.POST) # pylint: disable=attribute-defined-outside-init

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            if obj.position == 1:
                obj.groups.add(UserGroup.objects.get(name='admins'))
            if obj.position == 2:
                obj.groups.add(UserGroup.objects.get(name='developers'))

            obj.save()

            current_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(self.request, current_user)

            return HttpResponseRedirect(reverse('update_user', kwargs={'pk': obj.id}))

        return render(request, 'user/form.html', {'form': form})


class UpdateUserProfileView(UpdateView):
    """ Update User View Definition. """

    model = UserProfile
    form_class = UpdateUserProfileForm
    template_name = 'user/form.html'

    def dispatch(self, request, *args, **kwargs):
        self.obj = self.get_object()

        if (self.obj.id == request.user.id or self.request.user.is_admin) and self.obj.is_developer:
            return super(UpdateUserProfileView, self).dispatch(
                request,
                *args,
                **kwargs
            )
        if self.obj.id == request.user.id and self.request.user.is_admin:
            return super(UpdateUserProfileView, self).dispatch(
                request,
                *args,
                **kwargs
            )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('home')

    def get(self, request, *args, **kwargs):

        context = {
            'form': UpdateUserProfileForm(instance=self.obj),
            'title': 'Update User'
        }

        return render(request, 'user/form.html', context)


class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = "user/user_profile.html"
    context_object_name = 'profile'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserProfileDetailView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(UserProfile, username=self.kwargs.get('username'))
