from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, FormView

from apps.donations.models import Donation
from apps.projects.models import Project
from .forms import ProfileEditForm, DeleteAccountForm
from .models import User


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "account/profile.html"
    context_object_name = "profile_user"

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["my_projects"] = Project.objects.filter(creator=self.request.user).order_by("-created_at")
        ctx["my_donations"] = (
            Donation.objects.filter(donor=self.request.user)
            .select_related("project")
            .order_by("-created_at")
        )
        return ctx


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = "account/edit_profile.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)


class DeleteAccountView(LoginRequiredMixin, FormView):
    template_name = "account/delete_account_confirm.html"
    form_class = DeleteAccountForm
    success_url = reverse_lazy("homepage")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        logout(self.request)
        user.delete()
        messages.success(self.request, "Your account has been permanently deleted.")
        return super().form_valid(form)