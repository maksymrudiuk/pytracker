from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Local modules
from ..models import (
    Task,
    TimeJournal)
from ..forms import TimeJournalForm
from ..utils import paginate


class TimeJournalListView(ListView):
    model = TimeJournal
    template_name = "core/time_journal.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TimeJournalListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):

        if self.request.user.is_authenticated:
            queryset = TimeJournal.objects.all()
            if self.request.GET.get('task'):
                queryset = queryset.filter(task_id=self.request.GET.get('task'))
            if self.request.GET.get('project'):
                queryset = queryset.filter(task__project_id=self.request.GET.get('project'))
        else:
            queryset = TimeJournal.objects.none()

        return queryset

    def get_context_data(self, **kwargs):  # pylint: disable=arguments-differ
        context = super(TimeJournalListView, self).get_context_data(**kwargs)
        context = paginate(
            queryset=context['object_list'],
            pages=5,
            request=self.request,
            context=context,
            queryset_name='time_journals')

        return context

class TimeJournalCreateView(CreateView):
    """ Developers View definition. """
    model = TimeJournal

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TimeJournalCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        task = Task.objects.get(pk=kwargs['pk'])

        if not task.status == 3:

            context = dict()
            context['task'] = task
            context['form'] = TimeJournalForm
            return render(request, 'core/fix_time.html', context=context)

        url = reverse_lazy(
            'user_home',
            kwargs={
                'username': request.user.username
            }
        )
        return HttpResponseRedirect("%s?tip=tasks" % url)

    def post(self, request, *args, **kwargs):
        """ POST method processing. """

        form = TimeJournalForm(self.request.POST)

        if request.POST.get('cancel_btn'):
            messages.warning(request, 'Work is stoped')
            url = reverse_lazy(
                'user_home',
                kwargs={
                    'username': request.user.username
                }
            )
            return HttpResponseRedirect("%s?tip=tasks" % url)

        if form.is_valid():

            obj = form.save(commit=False)
            obj.task = Task.objects.get(pk=kwargs['pk'])
            obj.owner = request.user
            obj.save()

            messages.success(request, 'Time save')
            url = reverse_lazy(
                'user_home',
                kwargs={
                    'username': request.user.username
                }
            )
            return HttpResponseRedirect("%s?tip=tasks" % url)

        return render(request, 'core/fix_time.html', {'form': form})
