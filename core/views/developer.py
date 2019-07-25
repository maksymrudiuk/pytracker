""" This module include Views definition for Developer. """
# Django Imports
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Local modules
from user.models import UserProfile
from user.decorators import group_required
from ..models import Project, Developer
from ..utils import paginate

# from ..utils import paginate


class DevelopersView(TemplateView):
    """ Developers View definition. """
    template_name = 'core/free_developers_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DevelopersView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        developers = Project.objects.get(slug_id=kwargs['slug']).developers.all()
        users = UserProfile.objects.filter(position=2)

        context = super(DevelopersView, self).get_context_data(**kwargs)
        context['update_url'] = reverse_lazy(
            'free_developers_list',
            kwargs={
                'username': self.request.user.username,
                'slug': kwargs['slug']
            }
        )

        if not developers:
            context['developers'] = users
        else:
            context['developers'] = users.exclude(pk__in=developers)

        return context

    def post(self, request, *args, **kwargs):
        """ POST method processing. """
        data = request.POST

        user = UserProfile.objects.get(pk=data['pk'])
        project = Project.objects.get(slug_id=data['slug'])

        obj = Developer(
            user=user,
            project=project)
        obj.save()

        return JsonResponse({'key': 'success'})


class DevelopersAjaxDeleteView(SingleObjectMixin, View):
    """ Developers DeleteView definition. Ajax Deleting """

    model = Developer
    queryset = Developer.objects.all()

    @method_decorator(group_required("admins"), login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DevelopersAjaxDeleteView, self).dispatch(request, *args, **kwargs)

    def post(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ POST method processing. """
        self.object = self.get_object()  # pylint: disable=attribute-defined-outside-init
        self.object.delete()

        return JsonResponse({'key': 'success'})


class UserDevelopersListView(ListView):
    model = UserProfile
    template_name = "core/developers_list.html"

    @method_decorator(group_required("admins"), login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserDevelopersListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):

        if self.request.user.is_authenticated:
            queryset = UserProfile.objects.filter(position=2)
        else:
            queryset = UserProfile.objects.none()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserDevelopersListView, self).get_context_data(**kwargs)
        context = paginate(
            queryset=context['object_list'],
            pages=10,
            request=self.request,
            context=context,
            queryset_name='developers'
        )
        return context
