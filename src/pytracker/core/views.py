from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.http import JsonResponse

from django.template.defaultfilters import slugify

from .models import Project, Task, Comment, DeveloperInProject
from user.models import UserProfile
from .forms import (ProjectCreateForm,
                    TaskCreateForm,
                    TaskUpdateForm,
                    CommentForm)


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
            messages.success(request, 'Project successful created')
            return HttpResponseRedirect(reverse_lazy(
                'project_detail',
                kwargs={'slug': obj.slug_id}))

        return render(request, 'core/form.html', {'form': form})


class TaskCreateView(CreateView):  # pylint: disable=too-many-ancestors
    """ Task Create View definition. """

    model = Task

    def get(self, request, *args, **kwargs):

        context = {
            'form': TaskCreateForm,
            'title': 'Add Task'
        }

        return render(request, 'core/form.html', context)

    def post(self, request, *args, **kwargs):

        form = TaskCreateForm(self.request.POST)

        if form.is_valid:

            obj = form.save(commit=False)
            obj.creator = self.request.user
            obj.project = Project.objects.get(slug_id=self.kwargs['slug'])
            obj.save()
            return HttpResponseRedirect(reverse_lazy(
                'project_detail',
                kwargs={'slug': self.kwargs['slug']}))

        return render(request, 'core/form.html', {'form': form})


class TaskUpdateView(UpdateView):

    model = Task
    template_name = "core/form.html"
    form_class = TaskUpdateForm


    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'slug': self.kwargs['slug']})

    def post(self, request, *args, **kwargs):

        if request.POST.get('cancel_btn'):
            messages.warning(request, 'Task editing is canceled')
            return HttpResponseRedirect(reverse_lazy(
                'project_detail',
                kwargs={'slug': self.kwargs['slug']}))
        else:
            messages.success(request, 'Task successful saved')
            return super(TaskUpdateView, self).post(
                request,
                *args,
                **kwargs
            )


class TaskDetailView(DetailView):
    model = Task
    template_name = "core/task_detail.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Task.objects.filter(creator=self.request.user)
        else:
            queryset = Task.objects.none()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context['project_slug_id'] = self.kwargs['slug']
        context['comments'] = Comment.objects.filter(for_task=self.object)
        return context

class TaskDeleteView(DeleteView):  # pylint: disable=too-many-ancestors
    """ Task Delete View definition. """

    model = Task
    template_name = "core/confirm_delete.html"
    context_object_name = 'context'

    def get_context_data(self, **kwargs):
        context = super(TaskDeleteView, self).get_context_data(**kwargs)
        context['question'] = 'Do you want delete Task'
        context['title'] = 'Delete Task'
        context['context_url'] = 'delete_task'
        context['context_task_id'] = self.kwargs['pk']
        context['context_project_slug_id'] = self.kwargs['slug']
        return context

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'slug': self.kwargs['slug']})

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, 'Task deleting is canceled')
            return HttpResponseRedirect(reverse_lazy(
                'project_detail',
                kwargs={'slug': self.kwargs['slug']}))
        else:
            messages.success(request, 'Task successful delete')
            return super(TaskDeleteView, self).post(
                request,
                *args,
                **kwargs
            )


class CommentCreateView(CreateView):
    model = Comment

    def get(self, request, *args, **kwargs):

        context = {
            'form': CommentForm,
            'title': 'Add Comment'
        }
        return render(request, 'core/form.html', context=context)

    def post(self, request, *args, **kwargs):

        form = CommentForm(self.request.POST)

        if form.is_valid:
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.for_task = Task.objects.get(pk=kwargs['pk'])
            obj.save()
            return HttpResponseRedirect(reverse_lazy(
                'detail_task',
                kwargs={
                    'slug': kwargs['slug'],
                    'pk': kwargs['pk']
                }
            ))

        return render(request, 'core/form.html', {'form': form})

