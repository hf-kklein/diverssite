from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from .forms import SignupForm, ProfileForm

class Login(LoginView):
    template_name = "users/login.html"


class SignUp(generic.View):
    template_name = "users/signup.html"
    def post(self, request):
        signup_form = SignupForm(request.POST, request.FILES)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.save()
            return HttpResponseRedirect(reverse('users:thanks'))

        else:
            error = "please make sure your information are correct."
            context={
                     'signup_form': signup_form,
                     'error':error,
                     }
            return render(request,self.template_name, context)

    def get(self, request):
        signup_form = SignupForm()
        context={
                 'signup_form': signup_form,
                 }
        return render(request,self.template_name, context)

class RegComplete(generic.View):
    template_name = "users/thanks.html"
    def get(self, request):
        return render(request, self.template_name)



class Profile(LoginRequiredMixin,generic.DetailView):

    # print(selrequest)
    model = User
    login_url = '/users/login/'
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "users/profile.html"
    redirect_field_name = 'next'
    #
    def test_func(self, request, username):
        return self.request.user.username == username


    def get(self, request, username):
        print(self.request.user.username, username)
        context = {}
        return render(request,self.template_name, context)



    # SignupFormSet = formset_factory(SignupForm)
    # ProfileFormSet = formset_factory(ProfileForm)
    # if this is a POST request we need to process the form data
    # def post(self, request):
    #     # create a form instance and populate it with data from the request:
    #     signup_form = SignupForm(request.POST, request.FILES)
    #     # profile_formset = self.ProfileFormSet(request.POST, request.FILES,
    #     #                                  prefix='profile')
    #     # print(signup_formset.is_valid())
    #     # print(profile_formset.is_valid())
    #     # print("hello1")
    #     # check whether it's valid:
    #     if signup_form.is_valid():
    #         # process the data in form.cleaned_data as required
    #         # ...
    #         # redirect to a new URL:
    #         # print("hello")
    #         user = signup_form.save(commit=False)
    #         user.save()
    #         # for p in profile_formset:
    #         #     profile = p.save(commit=False)
    #         #     profile.user.add(user)
    #         #     profile.save()
    #         return HttpResponseRedirect(reverse('users:thanks'))
    #
    #     else:
    #         error = "please make sure your information are correct."
    #         context={'signup_form': signup_form,
    #                  'error':error,
    #                  # 'profile_formset': profile_formset
    #                  }
    #         return render(request,self.template_name, context)
