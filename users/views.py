from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import generic

from .forms import AddressForm, ProfileForm, ProfilePictureForm, SignupForm, UpdateUserForm
from .models import Profile, Settings


class Login(LoginView):
    template_name = "users/login.html"


class AccountActivateView:
    pass


class SignUpView(generic.View):
    template_name = "users/signup.html"

    def post(self, request):
        signup_form = SignupForm(request.POST, request.FILES)

        if (
            signup_form.is_valid()
            and signup_form.cleaned_data["validator"]
            == Settings.objects.values("registration_password")[0]["registration_password"]
        ):
            user = signup_form.save(commit=False)
            user.save()
            return HttpResponseRedirect(reverse("users:thanks"))

        else:
            print(
                signup_form.cleaned_data["validator"],
                Settings.objects.values("registration_password")[0]["registration_password"],
            )
            error = "please make sure your information are correct."
            context = {
                "signup_form": signup_form,
                "error": error,
            }
            return render(request, self.template_name, context)

    def get(self, request):
        signup_form = SignupForm()
        context = {
            "signup_form": signup_form,
        }
        return render(request, self.template_name, context)


class RegComplete(generic.View):
    template_name = "users/thanks.html"

    def get(self, request):
        return render(request, self.template_name)


class ProfileView(LoginRequiredMixin, generic.DetailView):
    # print(selrequest)
    model = User
    login_url = "/users/login/"
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "users/profile.html"
    redirect_field_name = "next"

    # def test_func(self, request, username):
    #     return self.request.user.username == username

    def setup_forms(self, u):
        try:
            self.profile = Profile.objects.get(user=u)
        except:
            self.profile = Profile.objects.create(user=u)

        self.updateuser_form = UpdateUserForm(instance=u, prefix="user")
        self.updateprofile_form = ProfileForm(instance=self.profile, prefix="profile")
        self.updateaddress_form = AddressForm(instance=self.profile, prefix="address")
        self.profilepicture_form = ProfilePictureForm(instance=self.profile, prefix="pic")

    def get(self, request):

        self.setup_forms(request.user)

        context = {
            "updateuser_form": self.updateuser_form,
            "updateprofile_form": self.updateprofile_form,
            "updateaddress_form": self.updateaddress_form,
            "profilepicture_form": self.profilepicture_form,
            "profile": self.profile,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        self.setup_forms(request.user)
        userform = UpdateUserForm(request.POST, request.FILES, instance=request.user, prefix="user")
        profileform = ProfileForm(request.POST, request.FILES, instance=self.profile, prefix="profile")
        addressform = AddressForm(request.POST, request.FILES, instance=self.profile, prefix="address")
        profilepictureform = ProfilePictureForm(request.POST, request.FILES, instance=self.profile, prefix="pic")
        print(profilepictureform)

        if userform.is_valid() and profileform.is_valid() and addressform.is_valid() and profilepictureform.is_valid():
            user = userform.save(commit=False)
            user.save()
            profile = profileform.save(commit=False)
            profile.save()
            address = addressform.save(commit=False)
            address.save()
            picture = profilepictureform.save(commit=False)
            picture.save()
            return HttpResponseRedirect(reverse("users:profile"))
        else:
            context = {
                "updateuser_form": userform,
                "updateprofile_form": profileform,
                "profilepicture_form": profilepictureform,
                "updateaddress_form": addressform,
                "profile": self.profile,
            }
            return render(request, self.template_name, context)
