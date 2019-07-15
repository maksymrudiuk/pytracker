# Django Imports
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.template.defaultfilters import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Local modules
from ..models import (
    Project,
    Task)
from ..forms import ProjectCreateForm
from ..utils import paginate


class ProjectListView(ListView):  # pylint: disable=too-many-ancestors
    """ ProjectList View definition. """
    model = Project
    template_name = "core/project_list.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context = paginate(
            queryset=context['object_list'],
            pages=5,
            request=self.request,
            context=context,
            queryset_name='projects')
        context['projects_page'] = 'active'
        return context


class ProjectDetailView(DetailView):  # pylint: disable=too-many-ancestors
    """ ProjectDetail View definition. """

    slug_field = 'slug_id'
    slug_url_kwarg = 'slug'


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectDetailView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):

        if self.request.user.is_authenticated:
            if self.request.user.is_admin:
                queryset = Project.objects.filter(owner=self.request.user)
            elif self.request.user.is_developer:
                queryset = Project.objects.filter(developers=self.request.user)
        else:
            queryset = Project.objects.none()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(project=self.object)
        return context


class ProjectCreateView(CreateView):  # pylint: disable=too-many-ancestors
    """ ProjectsCreate View definition. """

    model = Project

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectCreateView, self).dispatch(request, *args, **kwargs)

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
            messages.success(request, 'Project successful created')
            return HttpResponseRedirect(reverse_lazy(
                'project_detail',
                kwargs={'slug': obj.slug_id}))

        return render(request, 'core/form.html', {'form': form})
