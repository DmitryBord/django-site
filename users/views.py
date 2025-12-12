from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import get_user_model
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm

from django.shortcuts import render


# Create your views here.


class ProfileUser(LoginRequiredMixin, UpdateView):
    form_class = ProfileUserForm
    template_name = "users/profile.html"
    extra_context = {
        "title": "Профиль пользователя"
    }

    def get_success_url(self):
        return reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    model = get_user_model()
    template_name = "users/register.html"
    extra_context = {
        "title": "Регистрация"
    }
    success_url = reverse_lazy("users:login")


# def register_user(request):
#     if request.method == "POST":
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             form.instance.set_password(form.cleaned_data["password"])
#             form.save()
#             return render(request, "users/register_done.html")
#     else:
#         form = RegisterUserForm()
#     return render(request, 'users/register.html', {"form": form})


class LoginUsers(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"
    extra_context = {
        "title": "Авторизация"
    }
    #
    # def get_success_url(self):
    #     return reverse_lazy("home")

# def login_users(request):
#     if request.method == "POST":
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd["username"],
#                                 password=cd["password"])
#             if user and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse("home"))
#
#     form = LoginUserForm()
#     return render(request, "users/login.html",
#                   context={
#                       "title": "Авторизация",
#                       "form": form
#                   })


# def logout_users(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("users:login"))



class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change.html"

