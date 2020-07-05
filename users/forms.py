from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

#Sign Up Form
class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False,
                                 help_text='Optional',
                                 label='First Name')
    last_name = forms.CharField(max_length=30, required=False,
                                help_text='Optional',
                                label='Last Name')
    email = forms.EmailField(max_length=254,
                             label='E-Mail',
                             help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            ]

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'gender',
            'trikotnummer',
        ]

class AddressForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'street',
            'place',
            'zip',
        ]

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
          'picture',
        ]
