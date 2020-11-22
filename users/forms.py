from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div

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

    validator = forms.CharField(required=True, help_text="Dieses Passwort kannst du dir im Training oder bei anderen Mitgliedern erfragen")

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


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                'Personal Info:',
                Div(
                    Div('first_name', css_class="col-sm"),
                    Div('last_name', css_class="col-sm"),
                    css_class='row'
                ),
                Div(
                    Div('email', css_class="col-sm"),
                    css_class='row'
                )
            )
        )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            ]



class ProfileForm(forms.ModelForm):

    trikotnummer = forms.CharField(
        required=True,
        error_messages={'unique': 'Occupied :-( Check the wiki to see which numbers are still free'}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.error_text_inline = False
        self.helper.layout = Layout(
            Fieldset(
                'Divers Info:',
                Div(
                    Div('gender', css_class="col-sm"),
                    Div('trikotnummer', css_class="col-sm"),
                    css_class='row')
            )
        )

    class Meta:
        model = Profile
        fields = [
            'gender',
            'trikotnummer'
        ]


class AddressForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.error_text_inline = False
        self.helper.layout = Layout(
            Fieldset(
                'Connect:',
                Div(
                    Div('street', css_class="col-sm"),
                    Div('place', css_class="col-sm"),
                    Div('zip', css_class="col-sm"),
                    Div('mobile', css_class="col-sm"),
                    css_class='row'
                )
            )
        )

    class Meta:
        model = Profile
        fields = [
            'street',
            'place',
            'zip',
            'mobile',
        ]


class ProfilePictureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    class Meta:
        model = Profile
        fields = [
          'picture',
        ]
