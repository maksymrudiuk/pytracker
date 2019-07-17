# Django Imports
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
# Local modules
from ..models import Project, Task, TimeJournal
from ..utils import slice_queryset, paginate


# Create your views here.
class UserHomeView(View):
    """ Home View definition. """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserHomeView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """ Return context data into home page """

        context = {}
        tip = request.GET.get('tip')
        user = self.request.user
        projects = Project.objects.all()

        if user.is_authenticated:

            if tip is None:
                if user.is_admin:
                    projects = projects.filter(owner=user).order_by('-created_at')
                    context['developers'] = self.get_developers_list(projects)
                elif user.is_developer:
                    projects = projects.filter(developers=user).order_by('-created_at')

                context['title'] = 'Recently projects'
                context = slice_queryset(projects, context, 2, 'projects')

            if tip == 'projects':

                if user.is_admin:
                    projects = projects.filter(owner=user).order_by('-created_at')
                elif user.is_developer:
                    projects = projects.filter(developers=user).order_by('-created_at')

                context['title'] = 'Projects'

                context = paginate(
                    queryset=projects,
                    pages=5,
                    request=request,
                    context=context,
                    queryset_name='projects'
                )

            if tip == 'tasks':
                if user.is_developer:
                    tasks = Task.objects.filter(performer__user=request.user)

                    context['title'] = 'Tasks'

                    context = paginate(
                        queryset=tasks,
                        pages=5,
                        request=request,
                        context=context,
                        queryset_name='tasks'
                    )

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

@login_required
def home(request):
    return HttpResponseRedirect(reverse_lazy(
        'user_home',
        args=[request.user.username]))
