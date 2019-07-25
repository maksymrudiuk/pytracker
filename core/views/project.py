""" This module include Views definition for Project. """

# Django Imports
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)
from django.views.generic.detail import DetailView
from django.template.defaultfilters import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Local modules
from user.decorators import group_required
from ..models import (
    Project,
    Task,
    Developer)
from ..forms import ProjectCreateUpdateForm
from ..utils import paginate


class ProjectListView(ListView):  # pylint: disable=too-many-ancestors
    """ ProjectList View definition. """
    model = Project
    template_name = "core/projects.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):

        if self.request.user.is_authenticated:
            queryset = Project.objects.all()
        else:
            queryset = Project.objects.none()

        return queryset

    def get_context_data(self, **kwargs):  # pylint: disable=arguments-differ
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context = paginate(
            queryset=context['object_list'],
            pages=3,
            request=self.request,
            context=context,
            queryset_name='projects')

        return context


class ProjectDetailView(DetailView):  # pylint: disable=too-many-ancestors
    """ ProjectDetail View definition. """

    slug_field = 'slug_id'
    slug_url_kwarg = 'slug'
    template_name = 'core/project_detail.html'


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
        context['developers'] = Developer.objects.filter(project=self.object)

        return context


class ProjectCreateView(CreateView):  # pylint: disable=too-many-ancestors
    """ ProjectsCreate View definition. """

    model = Project

    @method_decorator(group_required("admins"), login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        context = {
            'form': ProjectCreateUpdateForm,
            'title': 'Create Project'
        }

        return render(request, 'core/form.html', context)

    def post(self, request, *args, **kwargs):

        form = ProjectCreateUpdateForm(self.request.POST)

        if request.POST.get('cancel_btn'):
            messages.warning(request, 'Project adding is canceled')
            url = reverse_lazy(
                'user_home',
                kwargs={
                    'username': request.user.username,
                }
            )

            return HttpResponseRedirect("%s?tip=projects" % url)

        if form.is_valid():

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
                kwargs={
                    'username': request.user.username,
                    'slug': obj.slug_id
                }
            ))

        return render(request, 'core/form.html', {'form': form})

class ProjectUpdateView(UpdateView):  # pylint: disable=too-many-ancestors
    """ ProjectUpdate View definition. """

    model = Project
    template_name = "core/form.html"
    form_class = ProjectCreateUpdateForm
    slug_field = 'slug_id'
    slug_url_kwarg = 'slug'

    @method_decorator(group_required("admins"), login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectUpdateView, self).dispatch(request, *args, **kwargs)

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
            messages.warning(request, 'Project editing is canceled')

            return HttpResponseRedirect(reverse_lazy(
                'project_detail',
                kwargs={
                    'username': self.request.user.username,
                    'slug': self.kwargs['slug']
                }
            ))
        else:
            messages.success(request, 'Project successful saved')

            return super(ProjectUpdateView, self).post(
                request,
                *args,
                **kwargs
            )


class ProjectDeleteView(DeleteView):  # pylint: disable=too-many-ancestors
    """ Project Delete View definition. """

    model = Project
    template_name = "core/confirm.html"
    context_object_name = 'context'
    slug_field = 'slug_id'
    slug_url_kwarg = 'slug'

    @method_decorator(group_required("admins"), login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectDeleteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectDeleteView, self).get_context_data(**kwargs)
        context['question'] = 'Do you want delete Project'
        context['title'] = 'Delete Project'
        context['context_url'] = 'project_delete'
        context['btn_class'] = 'danger'

        return context

    def get_success_url(self):
        url = reverse_lazy('user_home', kwargs={'username': self.request.user.username})
        return '%s?tip=projects' % url

    def post(self, request, *args, **kwargs):

        if request.POST.get('cancel_button'):
            messages.warning(request, 'Project deleting is canceled')

            return HttpResponseRedirect(reverse_lazy(
                'project_detail',
                kwargs={
                    'username': self.request.user.username,
                    'slug': self.kwargs['slug']
                }
            ))
        else:
            messages.success(request, 'Project successful delete')

            return super(ProjectDeleteView, self).post(
                request,
                *args,
                **kwargs
            )
