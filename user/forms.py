""" Forms definition for UserProfile Models """
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Field

from .models import UserProfile

class BaseSignUpUserProfileForm(forms.ModelForm):

    """ Base User Register Form. """

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        """ Meta definition for BaseSignUpUserProfile. """

        model = UserProfile
        fields = ('username', 'email', 'position')

    def __init__(self, *args, **kwargs):
        super(BaseSignUpUserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-md-4 control-label'
        self.helper.field_class = 'col-md-6'
        self.helper.add_input(Submit('submit', 'Sign Up'))

    def clean_password2(self):

        """ Check the two passwords for equality """

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
    """ Update User Profile Form. """

    class Meta:
        """ Meta definition for UpdateUserProfile. """

        model = UserProfile
        fields = ('first_name', 'last_name', 'photo', 'date_of_birth', )
        widgets = {
            'date_of_birth': forms.TextInput(attrs={'placeholder': '1999-01-01'}),
        }

    def __init__(self, *args, **kwargs):
        super(UpdateUserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-md-4 control-label'
        self.helper.field_class = 'col-md-6'
        self.helper.add_input(Submit('submit', 'Save'))
