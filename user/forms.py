from django import forms
from django.contrib import auth
from .models import Profile
from django.core.validators import ValidationError, EmailValidator

class LoginForm(forms.Form):
    id = forms.CharField(label='', max_length=20)
    password = forms.CharField(label='', max_length=20, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({'placeholder': ' Username', 'class':'login_box'})
        self.fields['password'].widget.attrs.update({'placeholder': ' Password', 'class':'login_box'})

class JoinForm(forms.Form):
    id = forms.CharField(label="ID ", max_length=20)
    password1 = forms.CharField(label="Password ", min_length=4, max_length=20, widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password(again) ", min_length=4, max_length=20, widget=forms.PasswordInput)
    email_address = forms.EmailField(label="Email Address ", error_messages={'invalid': 'Please enter a valid email address.'})

    def clean_id(self):
        # get_user_model helper Reference model classes through functions
        User = auth.get_user_model()
        
        # ID Duplicate
        if User.objects.filter(username=self.cleaned_data['id']).exists():
            raise ValidationError('ID is already in use.')
        return self.cleaned_data['id']

    def clean_password2(self):
        # Check the same password
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise ValidationError('Please enter the same password.')

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({'class': 'txtbox'})
        self.fields['password1'].widget.attrs.update({'class': 'txtbox'})
        self.fields['password2'].widget.attrs.update({'class': 'txtbox'})
        self.fields['email_address'].widget.attrs.update({'class': 'txtbox'})

class EditForm(forms.Form):
    password1 = forms.CharField(label="Password ", min_length=4, max_length=20, widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password(again) ", min_length=4, max_length=20, widget=forms.PasswordInput)
    email_address = forms.EmailField(label="Email Address ", error_messages={'invalid': 'Please enter a valid email address.'})

    def clean_password2(self):
        # Check the same password
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise ValidationError('Please enter the same password.')

        return self.cleaned_data
    
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)

        super(EditForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.initial['email_address'] = self.instance.email

        self.fields['password1'].widget.attrs.update({'class': 'txtbox'})
        self.fields['password2'].widget.attrs.update({'class': 'txtbox'})
        self.fields['email_address'].widget.attrs.update({'class': 'txtbox'})    
      
          
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number',)
        labels = {
            'phone_number' : 'Phone number '
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs.update({'class': 'txtbox'})
