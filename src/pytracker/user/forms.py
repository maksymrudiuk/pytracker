from django import forms
from .models import UserProfile

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class BaseSignUpUserProfileForm(forms.ModelForm):

    password1 = forms.CharField(label='Password',  widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password',  widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(BaseSignUpUserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-md-4 control-label'
        self.helper.field_class = 'col-md-6'
        self.helper.add_input(Submit('submit', 'Sign Up'))

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don`t match')
        return password2

    def save(self, commit=True):
        user = super(BaseSignUpUserProfileForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UpdateUserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'photo', 'date_of_birth', 'position')

    def __init__(self, *args, **kwargs):
        super(UpdateUserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-md-4 control-label'
        self.helper.field_class = 'col-md-6'
        self.helper.add_input(Submit('submit', 'Save'))