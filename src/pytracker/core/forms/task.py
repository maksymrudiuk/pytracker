from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from ..models import Task
from ..widgets import BootstrapDateTimePickerInput


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

    field_order = [
        'topic',
        'task_type',
        'priority',
        'start_date',
        'end_date',
        'estimated_time',
        'description',
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


class TaskUpdateForm(forms.ModelForm):
    """ Form definition to Update Task. """

    start_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=BootstrapDateTimePickerInput()
    )

    end_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=BootstrapDateTimePickerInput()
    )

    class Meta:
        """ Meta definition for TaskUpdateForm. """

        model = Task
        fields = [
            'topic',
            'task_type',
            'priority',
            'estimated_time',
            'description'
        ]

    field_order = [
        'topic',
        'task_type',
        'priority',
        'start_date',
        'end_date',
        'estimated_time',
        'description',
    ]

    def __init__(self, *args, **kwargs):
        super(TaskUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-md-4 control-label form-row'
        self.helper.field_class = 'col-md-6 form-row'
        self.helper.add_input(Submit(
            'save_btn',
            'Save',
            css_class='btn btn-success crispy-btn'))
        self.helper.add_input(Submit(
            'cancel_btn',
            'Cancel',
            css_class='btn btn-danger crispy-btn',
            formnovalidate='formnovalidate'))

    def save(self, commit=True):
        task = super(TaskUpdateForm, self).save(commit=False)
        task.start_date = self.cleaned_data['start_date']
        task.end_date = self.cleaned_data['end_date']
        if commit:
            task.save()
        return task
