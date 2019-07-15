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
# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required
# Local modules
from user.models import UserProfile
from ..models import (
    Project,
    Task,
    Comment)
from ..forms import (
    TaskCreateForm,
    TaskUpdateForm,
    CommentAddForm)
# from ..utils import paginate


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


class TaskUpdateView(UpdateView):  # pylint: disable=too-many-ancestors
    """ TaskUpdate View definition. """

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


class TaskDetailView(DetailView):  # pylint: disable=too-many-ancestors
    """ TaskDetail View definition. """

    model = Task
    template_name = "core/task_detail.html"

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
        context['developers'] = Project.objects.get(slug_id=self.kwargs['slug']).developers.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST

        task = Task.objects.get(pk=data['task_id'])
        task.performer = UserProfile.objects.get(pk=data['pk'])
        task.save()
        return JsonResponse({'key': 'success'})


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
