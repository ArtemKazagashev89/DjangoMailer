from django import forms

from .models import ClientManagement, Mailing, MailingAttempt, Message


class ClientManagementForm(forms.ModelForm):
    class Meta:
        model = ClientManagement
        fields = ["email", "full_name", "comment"]

    def __init__(self, *args, **kwargs):
        super(ClientManagementForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Введите электронную почту"})
        self.fields["full_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите Ф. И. О."})
        self.fields["comment"].widget.attrs.update({"class": "form-control", "placeholder": "Введите комментарий"})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields["subject"].widget.attrs.update({"class": "form-control", "placeholder": "Введите тему письма"})
        self.fields["body"].widget.attrs.update({"class": "form-control", "placeholder": "Введите содержание письма"})


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["message", "addressees"]

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields["message"].widget.attrs.update({"class": "form-control"})
        self.fields["addressees"].widget.attrs.update({"class": "form-check"})


class MailingAttemptForm(forms.ModelForm):
    class Meta:
        model = MailingAttempt
        fields = ["status", "mailing"]

    def __init__(self, *args, **kwargs):
        super(MailingAttemptForm, self).__init__(*args, **kwargs)
        self.fields["status"].widget.attrs.update({"class": "form-control"})
        self.fields["mailing"].widget.attrs.update({"class": "form-control"})
