from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("title", type=str, help="Заголовок сообщения для отправки")
        parser.add_argument(
            "--recipients",
            nargs="+",
            type=str,
            help="Список адресов электронной почты получателей",
        )
        parser.add_argument(
            "--message",
            type=str,
            help="Текст сообщения для отправки",
        )

    def handle(self, *args, **kwargs):
        title = kwargs["title"]
        message = kwargs["message"]
        recipients = kwargs.get("recipients")

        if not recipients:
            self.stdout.write(self.style.ERROR("Вы не указали адреса электронной почты получателей."))
            return

        self.__send_emails(title, message, recipients)

    def __send_emails(self, title, message, recipients):
        for receiver in recipients:
            try:
                send_mail(
                    subject=title,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[receiver],
                    fail_silently=False,
                )
            except BadHeaderError:
                self.__handle_exception("Неверный заголовок.", receiver, title)
            except Exception as e:
                self.__handle_exception(str(e), receiver, title)
            else:
                self.stdout.write(self.style.SUCCESS(f"Сообщение '{title}' отправлено '{receiver}' успешно"))

    def __handle_exception(self, error_message, receiver, title):
        self.stdout.write(self.style.ERROR(f"Сообщение '{title}' не удалось отправить '{receiver}': {error_message}"))
