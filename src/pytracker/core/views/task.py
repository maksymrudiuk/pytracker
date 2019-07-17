# Django Imports
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import (
    HttpResponseRedirect,
    JsonResponse)
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Local modules
from ..models import (
    Project,
    Task,
    Comment,
    Developer,
    TimeJournal)
from ..forms import (
    TaskCreateForm,
    TaskUpdateForm)


class TaskCreateView(CreateView):  # pylint: disable=too-many-ancestors
    """ Task Create View definition. """

    model = Task

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        context = {
            'form': TaskCreateForm,
            'title': 'Add Task'
        }

        return render(request, 'core/form.html', context)

    def post(self, request, *args, **kwargs):

        form = TaskCreateForm(self.request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = self.request.user
            obj.project = Project.objects.get(slug_id=self.kwargs['slug'])
            obj.save()
            return HttpResponseRedirect(reverse_lazy(
                'project_detail',
                kwargs={
                    'username': self.request.user.username,
                    'slug': self.kwargs['slug']
                }
            ))

        return render(request, 'core/form.html', {'form': form})


class TaskUpdateView(UpdateView):  # pylint: disable=too-many-ancestors
    """ TaskUpdate View definition. """

    model = Task
    template_name = "core/form.html"
    form_class = TaskUpdateForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'project_detail',
            kwargs={
                'username': self.request.user.username,
                'slug': self.kwargs['slug']
            }
        )

    def post(self, request, *args, **kwargs):

        if request.POST.get('cancel_btn'):
            messages.warning(request, 'Task editing is canceled')
            return HttpResponseRedirect(reverse_lazy(
                'project_detail',
                kwargs={
                    'username': self.request.user.username,
                    'slug': self.kwargs['slug']
                }
            ))
        else:
            messages.success(request, 'Task successful saved')
            return super(TaskUpdateView, self).post(
                request,
                *args,
                **kwargs
            )


class TaskDetailView(DetailView):  # pylint: disable=too-many-ancestors
    """ TaskDetail View definition. """

    model = Task
    template_name = "core/task_detail.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskDetailView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin:
                queryset = Task.objects.filter(creator=self.request.user)
            elif self.request.user.is_developer:
                queryset = Task.objects.filter(project__slug_id=self.kwargs['slug'])
        else:
            queryset = Task.objects.none()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context['project_slug_id'] = self.kwargs['slug']
        context['comments'] = Comment.objects.filter(for_task=self.object)
        if self.object.status == 3:
            context['spent_time'] = TimeJournal.objects.get(task=self.object).spent_time
        project = Project.objects.get(slug_id=self.kwargs['slug'])
        if self.request.user.is_admin:
            context['developers'] = Developer.objects.filter(project=project)
        elif self.request.user.is_developer:
            context['developer_id'] = Developer.objects.get(user=self.request.user).id

        return context

    def post(self, request, *args, **kwargs):
        data = request.POST

        task = Task.objects.get(pk=data['task_id'])
        task.performer = Developer.objects.get(pk=data['pk'])
        task.status = 2
        task.save()
        return JsonResponse({'key': 'success'})


class TaskDeleteView(DeleteView):  # pylint: disable=too-many-ancestors
    """ Task Delete View definition. """

    model = Task
    template_name = "core/confirm_delete.html"
    context_object_name = 'context'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskDeleteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TaskDeleteView, self).get_context_data(**kwargs)
        context['question'] = 'Do you want delete Task'
        context['title'] = 'Delete Task'
        context['context_url'] = 'delete_task'
        return context

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={
            'username': self.request.user.username,
            'slug': self.kwargs['slug']})

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, 'Task deleting is canceled')
            return HttpResponseRedirect(reverse_lazy(
                'project_detail',
                kwargs={
                    'username': self.request.user.username,
                    'slug': self.kwargs['slug']
                }
            ))
        else:
            messages.success(request, 'Task successful delete')
            return super(TaskDeleteView, self).post(
                request,
                *args,
                **kwargs
            )
