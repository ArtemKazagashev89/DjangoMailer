from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ClientManagementForm
from .models import ClientManagement, Mailing, MailingAttempt, Message


class HomeView(ListView):
    model = Mailing
    template_name = "mailsender/home.html"
    context_object_name = "home_data"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_mailings"] = Mailing.objects.count()
        context["active_mailings"] = Mailing.objects.filter(status=Mailing.LAUNCHED).count()
        context["unique_recipients"] = ClientManagement.objects.values("email").distinct().count()
        return context


class ClientManagementListView(ListView):
    model = ClientManagement
    template_name = "mailsender/clients_list.html"
    context_object_name = "clients"


class ClientManagementCreateView(CreateView):
    model = ClientManagement
    fields = ["full_name", "email"]
    template_name = "mailsender/client_form.html"
    success_url = reverse_lazy("mailsender:clients_list")

    def client_create(request):
        if request.method == "POST":
            form = ClientManagementForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("clients_list")
        else:
            form = ClientManagementForm()
        return render(request, "client_form.html", {"form": form})

    def client_update(request, pk):
        client = get_object_or_404(ClientManagement, pk=pk)  # Изменено на ClientManagement
        if request.method == "POST":
            form = ClientManagementForm(request.POST, instance=client)
            if form.is_valid():
                form.save()
                return redirect("clients_list")
        else:
            form = ClientManagementForm(instance=client)
        return render(request, "client_form.html", {"form": form})


class ClientManagementDetailView(DetailView):
    model = ClientManagement
    template_name = "mailsender/client_detail.html"
    context_object_name = "client"


class ClientManagementUpdateView(UpdateView):
    model = ClientManagement
    fields = ["full_name", "email"]
    template_name = "mailsender/client_form.html"
    success_url = reverse_lazy("mailsender:clients_list")


class ClientManagementDeleteView(DeleteView):
    model = ClientManagement
    template_name = "mailsender/client_confirm_delete.html"
    success_url = reverse_lazy("mailsender:clients_list")


class MessageListView(ListView):
    model = Message
    template_name = "mailsender/messages_list.html"
    context_object_name = "messages"


class MessageDetailView(DetailView):
    model = Message
    template_name = "mailsender/message_detail.html"
    context_object_name = "message"


class MessageCreateView(CreateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mailsender/message_form.html"
    success_url = reverse_lazy("mailsender:messages_list")


class MessageUpdateView(UpdateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mailsender/message_form.html"
    success_url = reverse_lazy("mailsender:messages_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "mailsender/message_confirm_delete.html"
    success_url = reverse_lazy("mailsender:messages_list")


class MailingListView(ListView):
    model = Mailing
    template_name = "mailsender/mailings_list.html"
    context_object_name = "mailings"


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "mailsender/mailing_detail.html"
    context_object_name = "mailing"


class MailingCreateView(CreateView):
    model = Mailing
    fields = ["status", "message", "addressees"]
    template_name = "mailsender/mailing_form.html"
    success_url = reverse_lazy("mailsender:mailings_list")


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ["status", "message"]
    template_name = "mailsender/mailing_form.html"
    success_url = reverse_lazy("mailsender:mailings_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailsender/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailsender:mailings_list")


class MailingSendView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        self.send_emails(mailing)
        self.update_status(mailing, Mailing.LAUNCHED)
        return redirect("mailsender:mailings_list")

    def send_emails(self, mailing):
        recipients = [recipient.email for recipient in mailing.addressees.all()]
        for receiver in recipients:
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[receiver],
                    fail_silently=False,
                )
                MailingAttempt.objects.create(
                    mailing=mailing, status="Success", server_answer=f"Email sent to {receiver}"
                )
            except BadHeaderError:
                self.handle_exception("Invalid header found.", receiver, mailing)
            except Exception as e:
                self.handle_exception(str(e), receiver, mailing)

    def handle_exception(self, error_message, receiver, mailing):
        MailingAttempt.objects.create(
            mailing=mailing,
            status="Failed",
            server_answer=f'Error occurred: "{error_message}" when sending to {receiver}',
        )

    def update_status(self, mailing, status):
        if mailing.status != status:
            mailing.status = status
            mailing.save()


class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = "mailsender/mailing_attempts_list.html"
    context_object_name = "mailing_attempts"
    ordering = ["-attempt_at"]

    def get_queryset(self):
        mailing_id = self.kwargs.get("mailing_id")
        return MailingAttempt.objects.filter(mailing__id=mailing_id).order_by("-attempt_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_id = self.kwargs.get("mailing_id")
        context["mailing"] = get_object_or_404(Mailing, id=mailing_id)
        return context
