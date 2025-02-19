from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import CustomUser


class FormValidatorMixin:
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен состоять только из цифр")
        return phone_number


class CustomUserCreationForm(FormValidatorMixin, UserCreationForm):
    phone_number = forms.CharField(
        max_length=15, required=False, help_text="Необязательное поле. Пожалуйста, введите номер телефона"
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "country", "phone_number", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Введите ваш email"})
        self.fields["country"].widget.attrs.update({"class": "form-control", "placeholder": "Введите вашу страну"})
        self.fields["phone_number"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите ваш номер телефона"}
        )
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Введите ваш пароль"})
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Подтвердите ваш пароль"}
        )


class EditProfileForm(FormValidatorMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["country", "phone_number", "avatar"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["country"].widget.attrs.update({"class": "form-control"})
        self.fields["phone_number"].widget.attrs.update({"class": "form-control"})
        self.fields["avatar"].widget.attrs.update({"class": "form-control"})


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Введите ваш email"})


class PasswordResetConfirmForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Новый пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Подтвердите новый пароль")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data
