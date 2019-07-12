from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView

from django.template.defaultfilters import slugify

from .models import Project, Task, Comment
from .forms import ProjectCreateForm, TaskCreateForm


# Create your views here.
class HomeView(View):
    """ Home View definition. """

    def get(self, request, *args, **kwargs):
        """ Return context data into home page """

        context = {}

        if self.request.user.is_authenticated:
            user = self.request.user
            context['projects'] = Project.objects.filter(owner=user)
            context['developers'] = self.get_developers_list(context['projects'])
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


class ProjectDetailView(DetailView):  # pylint: disable=too-many-ancestors
    """ ProjectDetail View definition. """

    slug_field = 'slug_id'
    slug_url_kwarg = 'slug'

    def get_queryset(self):

        if self.request.user.is_authenticated:
            queryset = Project.objects.filter(owner=self.request.user)
        else:
            queryset = Project.objects.none()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(project=self.object)
        return context


class ProjectsCreateView(CreateView):  # pylint: disable=too-many-ancestors
    """ ProjectsCreate View definition. """

    model = Project

    def get(self, request, *args, **kwargs):

        context = {
            'form': ProjectCreateForm,
            'title': 'Create Project'
        }

        return render(request, 'core/form.html', context)

    def post(self, request, *args, **kwargs):

        form = ProjectCreateForm(self.request.POST)

        if form.is_valid:

            # Pre save form
            obj = form.save(commit=False)
            # Save to create id then use id to format slud_id
            obj.save()

            # Add current user
            obj.owner = self.request.user
            # Add slud id
            obj.slug_id = slugify(obj.name) + '-' + str(obj.id)
            obj.save()
            return HttpResponseRedirect(reverse_lazy('home'))

        return render(request, 'core/form.html', {'form': form})


class TaskCreateView(CreateView):  # pylint: disable=too-many-ancestors
    """ TaskCreate View definition. """

    model = Task

    def get(self, request, *args, **kwargs):

        context = {
            'form': TaskCreateForm,
            'title': 'Create Task'
        }

        return render(request, 'core/form.html', context)

    def post(self, request, *args, **kwargs):

        form = TaskCreateForm(self.request.POST)

        if form.is_valid:

            obj = form.save(commit=False)
            print(dir(obj))
            print(obj.end_date)
            obj.creator = self.request.user
            obj.project = Project.objects.get(slug_id=self.kwargs['slug'])
            obj.save()
            return HttpResponseRedirect(reverse_lazy('home'))

        return render(request, 'core/form.html', {'form': form})
