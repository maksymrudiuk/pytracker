# Django Imports
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Local modules
from ..models import Project
# from .utils import paginate


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
                context['projects'] = Project.objects.filter(owner=user)
                context['developers'] = self.get_developers_list(context['projects'])
            elif self.request.user.is_developer:
                context['projects'] = Project.objects.filter(developers=self.request.user)

            context['home_page'] = 'active'


            return render(request, 'core/overview.html', context=context)

        return render(request, 'core/overview.html', context=None)

    @staticmethod
    def get_developers_list(projects):
        """ Get developers list for user """
        teams = [p.developers.all() for p in projects]
        developers = set()
        for team in teams:
            for developer in team:
                developers.add(developer)

        return developers
