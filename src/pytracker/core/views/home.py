# Django Imports
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Local modules
from ..models import Project
# from ..utils import paginate


# Create your views here.
class HomeView(View):
    """ Home View definition. """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """ Return context data into home page """

        context = {}

        if self.request.user.is_authenticated:

            if self.request.user.is_admin:
                user = self.request.user
                projects_queryset = Project.objects.filter(owner=user).order_by('created_at')
                context['developers'] = self.get_developers_list(projects_queryset)
            elif self.request.user.is_developer:
                projects_queryset = Project.objects.filter(
                    developers=self.request.user).order_by('created_at')

            if len(projects_queryset) > 4:
                context['projects'] = projects_queryset[:4]
                context['has_other'] = True
            else:
                context['projects'] = projects_queryset
                context['has_other'] = False

            context['home_page'] = 'active'


            return render(request, 'core/home.html', context=context)

        return render(request, 'core/home.html', context=None)

    @staticmethod
    def get_developers_list(projects):
        """ Get developers list for user """
        teams = [p.developers.all() for p in projects]
        developers = set()
        for team in teams:
            for developer in team:
                developers.add(developer)

        return developers
