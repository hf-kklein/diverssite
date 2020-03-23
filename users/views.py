from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from .forms import SignupForm, ProfileForm, UpdateUserForm, AddressForm
from .models import Profile

class Login(LoginView):
    template_name = "users/login.html"


class SignUpView(generic.View):
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



class ProfileView(LoginRequiredMixin,generic.DetailView):

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

    def setup_forms(self, username):
        self.user = User.objects.get(username = username)
        try:
            self.profile = Profile.objects.get(user = self.user)
            print("profile for user X exists")
        except:
            self.profile = Profile.objects.create(user = self.user)
            print("profile for user X created")

        self.updateuser_form = UpdateUserForm(instance=self.user, prefix="user")
        self.updateprofile_form = ProfileForm(instance=self.profile, prefix="profile")
        self.updateaddress_form = AddressForm(instance=self.profile, prefix="address")

    def get(self, request, username):
        self.setup_forms(username)
        context = {
                   'updateuser_form':self.updateuser_form,
                   'updateprofile_form':self.updateprofile_form,
                   'updateaddress_form':self.updateaddress_form,
        }
        return render(request,self.template_name, context)

    def post(self, request, username):
        self.setup_forms(username)
        userform = UpdateUserForm(request.POST, request.FILES, instance=self.user, prefix="user")
        profileform = ProfileForm(request.POST, request.FILES, instance=self.profile, prefix="profile")
        addressform = AddressForm(request.POST, request.FILES, instance=self.profile, prefix="address")


        print(userform, profileform)
        if userform.is_valid() and profileform.is_valid() and addressform.is_valid():
            user = userform.save(commit=False)
            user.save()
            profile = profileform.save(commit=False)
            profile.save()
            address = addressform.save(commit=False)
            address.save()
        return HttpResponseRedirect(reverse('users:profile', args=[username]))


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
