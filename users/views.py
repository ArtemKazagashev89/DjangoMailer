# users/views.py
import secrets

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, View
from django.views.generic.edit import FormView

from .forms import EditProfileForm, CustomUserCreationForm, PasswordResetRequestForm
from .models import CustomUser
from .services import CACHE_TIMEOUT, CustomUserService


def email_verification(token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class CustomLoginView(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy("mailsender:home")

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при входе. Проверьте свои учетные данные.")
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    template_name = "logout.html"
    next_page = reverse_lazy("users:logout")


class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy("mailsender:home")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        return super().form_valid(form)


class EditProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = EditProfileForm
    template_name = "edit_profile.html"

    def get_success_url(self):
        messages.success(
            self.request, f"Профиль успешно обновлён. Изменения будут отображены через {CACHE_TIMEOUT} секунд."
        )
        return reverse_lazy("users:user_profile", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.request.user.pk)


class UsersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "users.view_customuser"
    model = CustomUser
    template_name = "all_users.html"
    context_object_name = "users"

    def get_queryset(self):
        return CustomUserService.get_all_users().filter(pk=self.request.user.pk).order_by("id")


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "user_profile.html"
    context_object_name = "user_profile"

    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["CACHE_TIMEOUT"] = CACHE_TIMEOUT
        return context


class ChangeUserStatusView(PermissionRequiredMixin, View):
    permission_required = "users.can_block_user"

    def post(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        if user == request.user:
            messages.warning(request, "Вы не можете заблокировать себя.")
            return redirect("users:all_users")
        user.is_active = not user.is_active
        user.save()
        return redirect("users:all_users")


class PasswordResetRequestView(View):
    def get(self, request):
        form = PasswordResetRequestForm()
        return render(request, "password_reset_request.html", {"form": form})

