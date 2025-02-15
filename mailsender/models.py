from django.db import models
from django.contrib.auth import get_user_model


class ClientManagement(models.Model):
    email = models.EmailField(max_length=100, unique=True, verbose_name="Электронная почта")
    full_name = models.CharField(max_length=150, verbose_name="Ф. И. О.")
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Владелец")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"


class Message(models.Model):
    subject = models.CharField(max_length=200, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Содержание письма")
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Владелец")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Mailing(models.Model):
    COMPLETED = "Completed"
    CREATED = "Created"
    LAUNCHED = "Launched"

    dispatch_status = [
        (COMPLETED, "Завершена"),
        (CREATED, "Создана"),
        (LAUNCHED, "Запущена"),
    ]

    first_sending = models.DateTimeField(verbose_name="Дата отправки первого письма", auto_now_add=True)
    end_sending = models.DateTimeField(verbose_name="Дата окончания отправки", auto_now=True)
    status = models.CharField(max_length=20, choices=dispatch_status, default=CREATED, verbose_name="Статус")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    addressees = models.ManyToManyField(ClientManagement)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Владелец")

    def __str__(self):
        message_subject = self.message.subject if self.message else "Без темы"
        return f"{message_subject} {self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class MailingAttempt(models.Model):
    SUCCESS = "success"
    FAILED = "failed"

    status_choices = [(SUCCESS, "успешно"), (FAILED, "не успешно")]

    attempt_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.CharField(max_length=10, choices=status_choices, verbose_name="Статус")
    server_answer = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Владелец")

    def __str__(self):
        return f"{self.mailing}: {self.status} ({self.attempt_at})"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"

