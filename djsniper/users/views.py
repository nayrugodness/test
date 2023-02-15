from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.generic import DetailView, RedirectView, UpdateView
from .models import User, Order
from .forms import UserPersonalCreationForm, UserEnterpriseCreationForm, UserChangeForm, UserChangePassword
from django import forms


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "users/dashboard.html"


user_detail_view = UserDetailView.as_view()


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "users/user_detail.html"


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserPasswordUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserChangePassword
    template_name = "users/password.html"


user_password_view = UserPasswordUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={
            "username": self.request.user.username
        })


user_redirect_view = UserRedirectView.as_view()


class UserPersonalCreateView(generic.CreateView):
    template_name = "account/signup_personal.html"

    # model = User
    form_class = UserPersonalCreationForm

    def form_valid(self, form):
        instance = form.save()
        return redirect("sniper:home")


Role = (
    ('Persona Natural', 'Persona Natural'),
    ('Empresa', 'Empresa'),
    ('Administrador', 'Administrador'),
    ('Desarrollador', 'Desarrollador')
)


class UserEnterpriseCreateView(generic.CreateView):
    template_name = "account/signup_enterprise.html"
    form_class = UserEnterpriseCreationForm
    # model = User
    success_message = _("Informaton successfully updated")
    initial = {
        "role": "Empresa"
    }

    def form_valid(self, form):
        instance = form.save()
        return redirect("sniper:home")


class OrderCreateView(generic.CreateView):
    template_name = "sniper/order_create.html"
    form_class = Order
    success_message = _("Tu orden ha sido listada")
