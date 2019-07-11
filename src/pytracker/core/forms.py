from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import Project
from user.models import UserProfile


class ProjectCreateForm(forms.ModelForm):

    class Meta:
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