from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Profile
from .forms import SignUpForm, ProfileForm

class Login(LoginView):
    template_name = "users/login.html"


class SignUp(generic.View):
    template_name = "users/signup.html"
    # if this is a POST request we need to process the form data
    def post(self, request):
        # create a form instance and populate it with data from the request:
        form_signup = SignUpForm(request.POST)
        form_profile = ProfileForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            user = form.save(commit=False)
            user.save()
            return HttpResponseRedirect('/thanks/')

        return render(request, self.template_name, context={'form': form})

    # if a GET (or any other method) we'll create a blank form
    def get(self, request):
        form_signup = SignUpForm()
        form_profile = ProfileForm()
        context={'form_signup': form_signup,
                 'form_profile':form_profile}
        print(context)
        return render(request,self.template_name, context)

class RegComplete(generic.View):
    template_name = "users/thanks.html"
    def get(self, request):
        return render(request, self.template_name)
