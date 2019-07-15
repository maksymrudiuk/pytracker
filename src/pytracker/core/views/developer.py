# Django Imports
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Local modules
from user.models import UserProfile
from ..models import Project, DeveloperInProject
# from ..utils import paginate


class DevelopersView(TemplateView):
    """ Developers View definition. """
    template_name = 'core/developers_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DevelopersView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        developers_in_project = Project.objects.get(slug_id=kwargs['slug']).developers.all()
        developers = UserProfile.objects.filter(position=2)

        context = super(DevelopersView, self).get_context_data(**kwargs)
        context['update_url'] = reverse_lazy(
            'add_developer_in_project',
            kwargs={'slug': kwargs['slug']})
        context['project_slug_id'] = kwargs['slug']

        if not developers_in_project:
            context['developers'] = developers
        else:
            context['developers'] = developers.exclude(pk__in=developers_in_project)

        return context

    def post(self, request, *args, **kwargs):
        """ POST method processing. """
        data = request.POST

        developer = UserProfile.objects.get(pk=data['pk'])
        project = Project.objects.get(slug_id=data['slug'])

        obj = DeveloperInProject(
            developer=developer,
            project=project)
        obj.save()
        return JsonResponse({'key': 'success'})