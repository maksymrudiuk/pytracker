# Django Imports
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Local modules
from ..models import (
    Task,
    Comment)
from ..forms import CommentAddForm
# from ..utils import paginate


class CommentCreateView(CreateView):  # pylint: disable=too-many-ancestors
    """ Comment View definition. """

    model = Comment

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CommentCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        context = {
            'form': CommentAddForm,
            'title': 'Add Comment'
        }
        return render(request, 'core/form.html', context=context)

    def post(self, request, *args, **kwargs):

        form = CommentAddForm(self.request.POST)

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
