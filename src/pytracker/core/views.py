from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView

from django.template.defaultfilters import slugify

from .models import Project, Task, Comment, DeveloperInProject
from .forms import ProjectCreateForm

# Create your views here.
class HomeView(View):

    def get(self, request, *args, **kwargs):

        context = {}

        if self.request.user.is_authenticated:
            user = self.request.user
            context['projects'] = Project.objects.filter(owner=user)
            context['developers'] = self.get_developers_list(context['projects'])
            return render(request, 'core/overview.html', context=context)
        else:
            return render(request, 'core/overview.html', context=None)

    def get_developers_list(self, projects):

        teams = [p.developers.all() for p in projects]
        developers = set()
        for team in teams:
            for developer in team:
                developers.add(developer)

        return developers

class ProjectDetailView(DetailView):

    slug_field = 'slug_id'
    slug_url_kwarg = 'slug'

    def get_queryset(self):

        if self.request.user.is_authenticated:
            queryset = Project.objects.filter(owner=self.request.user)
        else:
            queryset = Project.objects.none()

        return queryset



class ProjectsCreateView(CreateView):

    model = Project

    def get(self, request, *args, **kwargs):

        context = {
            'form': ProjectCreateForm,
            'title': 'Create Project'
        }

        return render(request, 'core/form.html', context)

    def post(self, request, *args, **kwargs):

        form = ProjectCreateForm(request.POST)

        if form.is_valid:

            # Pre save form
            obj = form.save(commit=False)
            obj.save() # Save to create id then use id to format slud_id

            # Add current user
            obj.owner = self.request.user
            # Add slud id
            obj.slug_id = slugify(obj.name) + '-' + str(obj.id)
            obj.save()
            return HttpResponseRedirect(reverse_lazy('home'))

        return render(request, 'core/form.html', {'form': form})