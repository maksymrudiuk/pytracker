from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Project, Task
from user.models import UserProfile
from .widgets import BootstrapDateTimePickerInput


class ProjectCreateForm(forms.ModelForm):
    """ Form definition for Project. """

    class Meta:
        """ Meta definition for ProjectCreateForm. """

        model = Project
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(ProjectCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-md-4 control-label form-row'
        self.helper.field_class = 'col-md-6 form-row'
        self.helper.add_input(Submit('submit', 'Add'))


class TaskCreateForm(forms.ModelForm):
    """ Form definition for Task. """

    start_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=BootstrapDateTimePickerInput()
    )

    end_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=BootstrapDateTimePickerInput()
    )

    class Meta:
        """ Meta definition for TaskCreateForm. """

        model = Task
        fields = [
            'topic',
            'task_type',
            'priority',
            'estimated_time',
            'description'
        ]

    def __init__(self, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-md-4 control-label form-row'
        self.helper.field_class = 'col-md-6 form-row'
        self.helper.add_input(Submit('submit', 'Add'))

    def save(self, commit=True):
        task = super(TaskCreateForm, self).save(commit=False)
        task.start_date = self.cleaned_data['start_date']
        task.end_date = self.cleaned_data['end_date']
        if commit:
            task.save()
        return task
