from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .forms import ClientManagementForm
from .models import ClientManagement, Mailing, Message, MailingAttempt


class HomeView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailsender/home.html"
    context_object_name = "home_data"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_mailings"] = Mailing.objects.filter(owner=self.request.user).count()
        context["active_mailings"] = Mailing.objects.filter(owner=self.request.user, status=Mailing.LAUNCHED).count()
        context["unique_recipients"] = (
            ClientManagement.objects.filter(owner=self.request.user).values("email").distinct().count()
        )
        return context


class ClientManagementListView(LoginRequiredMixin, ListView):
    model = ClientManagement
    template_name = "mailsender/clients_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        return ClientManagement.objects.filter(owner=self.request.user)


class ClientManagementCreateView(LoginRequiredMixin, CreateView):
    model = ClientManagement
    form_class = ClientManagementForm
    template_name = "mailsender/client_form.html"
    success_url = reverse_lazy("mailsender:clients_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Клиент успешно создан.")
        return super().form_valid(form)


class ClientManagementDetailView(LoginRequiredMixin, DetailView):
    model = ClientManagement
    template_name = "mailsender/client_detail.html"
    context_object_name = "client"

    def get_queryset(self):
        return ClientManagement.objects.filter(owner=self.request.user)


class ClientManagementUpdateView(LoginRequiredMixin, UpdateView):
    model = ClientManagement
    form_class = ClientManagementForm
    template_name = "mailsender/client_form.html"
    success_url = reverse_lazy("mailsender:clients_list")

    def get_queryset(self):
        return ClientManagement.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Клиент успешно обновлён.")
        return super().form_valid(form)


class ClientManagementDeleteView(LoginRequiredMixin, DeleteView):
    model = ClientManagement
    template_name = "mailsender/client_confirm_delete.html"
    success_url = reverse_lazy("mailsender:clients_list")

    def get_queryset(self):
        return ClientManagement.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Клиент успешно удалён.")
        return super().delete(request, *args, **kwargs)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailsender/messages_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mailsender/message_form.html"
    success_url = reverse_lazy("mailsender:messages_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Сообщение успешно создано.")
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mailsender/message_form.html"
    success_url = reverse_lazy("mailsender:messages_list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Сообщение успешно обновлено.")
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailsender/message_confirm_delete.html"
    success_url = reverse_lazy("mailsender:messages_list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Сообщение успешно удалено.")
        return super().delete(request, *args, **kwargs)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailsender/mailings_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailsender/mailing_detail.html"
    context_object_name = "mailing"

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    fields = ["status", "message", "addressees"]
    template_name = "mailsender/mailing_form.html"
    success_url = reverse_lazy("mailsender:mailings_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Рассылка успешно создана.")
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    fields = ["status", "message"]
    template_name = "mailsender/mailing_form.html"
    success_url = reverse_lazy("mailsender:mailings_list")

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Рассылка успешно обновлена.")
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailsender/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailsender:mailings_list")

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Рассылка успешно удалена.")
        return super().delete(request, *args, **kwargs)


class MailingSendView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk, owner=request.user)
        self.send_mailing(mailing)
        messages.success(request, "Рассылка успешно отправлена.")
        return redirect("mailsender:mailings_list")

    def send_mailing(self, mailing):
        for recipient in mailing.addressees.all():
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient.email],
                    fail_silently=False,
                )
                messages.success(self.request, f"Сообщение успешно отправлено на {recipient.email}.")
            except BadHeaderError:
                messages.error(self.request, f"Неверный заголовок для {recipient.email}.")
            except Exception as e:
                messages.error(self.request, f"Ошибка при отправке на {recipient.email}: {str(e)}")


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = "mailsender/mailing_attempts_list.html"
    context_object_name = "mailing_attempts"
    ordering = ["-attempt_at"]

    def get_queryset(self):
        mailing_id = self.kwargs.get("mailing_id")
        return MailingAttempt.objects.filter(mailing__id=mailing_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_id = self.kwargs.get("mailing_id")
        context["mailing"] = get_object_or_404(Mailing, id=mailing_id, owner=self.request.user)
        return context
