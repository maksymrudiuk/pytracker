from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Local modules
from ..models import (
    Task,
    TimeJournal)

from ..forms import TimeJournalForm


class TimeJournalView(CreateView):
    """ Developers View definition. """
    model = TimeJournal

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TimeJournalView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        context = dict()
        context['task'] = Task.objects.get(pk=kwargs['pk'])
        context['form'] = TimeJournalForm
        return render(request, 'core/fix_time.html', context=context)

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
            task = Task.objects.get(pk=kwargs['pk'])
            # Update Task Status
            task.status = 3
            task.save()

            obj = form.save(commit=False)
            obj.task = task
            obj.save()

            messages.success(request, 'Task is completed')
            url = reverse_lazy(
                'user_home',
                kwargs={
                    'username': request.user.username
                }
            )
            return HttpResponseRedirect("%s?tip=tasks" % url)

        return render(request, 'core/fix_time.html', {'form': form})