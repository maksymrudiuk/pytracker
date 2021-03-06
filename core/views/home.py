""" This module include View definition for Overview home page. """
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

        if user.is_authenticated:

            if tip is None:

                if user.is_admin or user.is_superuser:
                    projects = Project.objects.filter(owner=user).order_by('-created_at')
                    context['developers'] = self.get_developers_list(projects)
                elif user.is_developer:
                    projects = Project.objects.filter(developers=user).order_by('-created_at')

                context['title'] = 'Recently projects'
                context = slice_queryset(projects, context, 2, 'projects')

            if tip == 'projects':

                if user.is_admin or user.is_superuser:
                    projects = Project.objects.filter(owner=user).order_by('-created_at')
                elif user.is_developer:
                    projects = Project.objects.filter(developers=user).order_by('-created_at')

                context['title'] = 'Projects'
                context = paginate(
                    queryset=projects,
                    pages=3,
                    request=request,
                    context=context,
                    queryset_name='projects'
                )

            if tip == 'tasks':

                if user.is_developer:
                    tasks = Task.objects.filter(performer=request.user).order_by('status')
                    context['title'] = 'Tasks'
                    context = paginate(
                        queryset=tasks,
                        pages=5,
                        request=request,
                        context=context,
                        queryset_name='tasks'
                    )

            if tip == 'time_managment':

                if user.is_developer:
                    time_journals = TimeJournal.objects.filter(owner=request.user)
                if user.is_admin:
                    tasks = Task.objects.filter(creator=request.user)
                    time_journals = TimeJournal.objects.filter(task__in=tasks)

                context['title'] = 'Time Managment'

                context = paginate(
                    queryset=time_journals,
                    pages=5,
                    request=request,
                    context=context,
                    queryset_name='time_journals'
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
    """Redirect main home view"""

    return HttpResponseRedirect(reverse_lazy(
        'user_home',
        args=[request.user.username]))
