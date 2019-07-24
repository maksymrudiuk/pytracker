""" This module include Views definition for Task model. """
# Django Imports
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import (
    HttpResponseRedirect,
    JsonResponse)
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Local modules
from user.decorators import group_required
from user.models import UserProfile
from ..models import (
    Project,
    Task,
    Comment,
    Developer,
    TimeJournal,)
from ..forms import TaskCreateUpdateForm


class TaskCreateView(CreateView):  # pylint: disable=too-many-ancestors
    """ Task Create View definition. """

    model = Task

    @method_decorator(group_required("admins"), login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        context = {
            'form': TaskCreateUpdateForm,
            'title': 'Add Task'
        }

        return render(request, 'core/form.html', context)

    def post(self, request, *args, **kwargs):

        form = TaskCreateUpdateForm(self.request.POST)

        if request.POST.get('cancel_btn'):
            messages.warning(request, 'Task adding is canceled')
            return HttpResponseRedirect(reverse_lazy(
                'project_detail',
                kwargs={
                    'username': self.request.user.username,
                    'slug': self.kwargs['slug']
                }
            ))

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
    form_class = TaskCreateUpdateForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()  # pylint: disable=attribute-defined-outside-init
        if self.object.status == 3:
            messages.warning(request, 'Task is not editable after completed. You can only delete.')
            return HttpResponseRedirect(reverse_lazy(
                'project_detail',
                kwargs={
                    'username': self.request.user.username,
                    'slug': self.kwargs['slug']
                }
            ))
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
        context['comments'] = Comment.objects.filter(for_task=self.object).order_by('-date_of_add')
        if self.object.status == 3:
            time_journals = TimeJournal.objects.filter(task=self.object)
            context['spent_time'] = sum([obj.spent_time for obj in time_journals])
        project = Project.objects.get(slug_id=self.kwargs['slug'])
        if self.request.user.is_admin:
            developers = Developer.objects.filter(project=project)
            context['developers'] = [d.user for d in developers]
        # elif self.request.user.is_developer:
        #     context['developer_id'] = Developer.objects.get(user=self.request.user, project=project).id

        return context

    def post(self, request, *args, **kwargs):
        """ Ajax request proccessing """

        data = request.POST
        task = Task.objects.get(pk=data['task_id'])

        if task.status == 3:
            return JsonResponse({'key': 'error'})

        task.performer = UserProfile.objects.get(pk=data['pk'])
        task.status = 2
        task.save()

        return JsonResponse({'key': 'success'})


class TaskDeleteView(DeleteView):  # pylint: disable=too-many-ancestors
    """ Task Delete View definition. """

    model = Task
    template_name = "core/confirm.html"
    context_object_name = 'context'

    @method_decorator(group_required("admins"), login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskDeleteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TaskDeleteView, self).get_context_data(**kwargs)
        context['question'] = 'Do you want delete Task'
        context['title'] = 'Delete Task'
        context['context_url'] = 'delete_task'
        context['btn_class'] = 'danger'
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


class TaskStatusUpdateView(TemplateView):
    template_name = 'core/confirm.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskStatusUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TaskStatusUpdateView, self).get_context_data(**kwargs)
        context['context'] = Task.objects.get(pk=kwargs['pk']).topic
        context['question'] = 'Do you want finish Task'
        context['title'] = 'Finish Task'
        context['context_url'] = 'finish_task'
        context['btn_class'] = 'success'
        return context


    def post(self, request, *args, **kwargs):

        if request.POST.get('confirm_button'):
            task = Task.objects.get(pk=kwargs['pk'])
            task.status = 3
            task.save()
            messages.success(request, 'Task is finish')
            url = reverse_lazy(
                'user_home',
                kwargs={
                    'username': self.request.user.username
                }
            )
            return HttpResponseRedirect("%s?tip=time_managment" % url)

        elif request.POST.get('cancel_button'):
            messages.warning(request, 'Task status update is cancel.')
            url = reverse_lazy(
                'user_home',
                kwargs={
                    'username': request.user.username,
                }
            )
            return HttpResponseRedirect("%s?tip=tasks" % url)
