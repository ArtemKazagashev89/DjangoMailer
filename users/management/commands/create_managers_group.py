from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates Managers group"

    def handle(self, *args, **options):
        managers_group = Group.objects.create(name="Manager")
        block_user_permission = Permission.objects.get(codename="can_block_user")
        disable_mailing_permission = Permission.objects.get(codename="can_disable_mailing")
        view_mailing_unit_permission = Permission.objects.get(codename="view_mailingunit")
        view_user_permission = Permission.objects.get(codename="view_customuser")
        view_mail_receiver = Permission.objects.get(codename="view_mailreceiver")
        view_report = Permission.objects.get(codename="can_view_report")
        managers_group.permissions.add(
            block_user_permission,
            disable_mailing_permission,
            view_mailing_unit_permission,
            view_user_permission,
            view_mail_receiver,
            view_report,
        )

        self.stdout.write(self.style.SUCCESS(f"Successfully created Group {managers_group.name}"))
