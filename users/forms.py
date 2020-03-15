from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

#Sign Up Form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False,
                                 help_text='Optional',
                                 label = 'First Name')
    last_name = forms.CharField(max_length=30, required=False,
                                help_text='Optional',
                                label = 'Last Name')
    email = forms.EmailField(max_length=254,
                             label = 'E-Mail',
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

class ProfileForm(forms.Form):
    trikotnummer = forms.CharField(max_length=3, required=False)
    gender = forms.CharField( max_length= 10, required=False)

    class Meta:
        model = Profile
        fields = [
            'gender',
            'trikotnummer',
        ]
