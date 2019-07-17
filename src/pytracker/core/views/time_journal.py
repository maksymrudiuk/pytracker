from django.shortcuts import render
# from django.contrib import messages
# from django.urls import reverse_lazy
# from django.http import (
#     HttpResponseRedirect,
#     JsonResponse)
# from django.views.generic.edit import (
#     CreateView,
#     UpdateView,
#     DeleteView)
# from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Local modules
from ..models import (
    Task,
    TimeJournal)


class TimeJournalView(TemplateView):
    """ Developers View definition. """
    template_name = 'core/fix_time.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TimeJournalView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(TimeJournalView, self).get_context_data(**kwargs)
        context['task'] = Task.objects.get(pk=kwargs['pk'])

        return context

    # def post(self, request, *args, **kwargs):
    #     """ POST method processing. """
    #     data = request.POST

    #     user = UserProfile.objects.get(pk=data['pk'])
    #     project = Project.objects.get(slug_id=data['slug'])

    #     obj = Developer(
    #         user=user,
    #         project=project)
    #     obj.save()
    #     return JsonResponse({'key': 'success'})