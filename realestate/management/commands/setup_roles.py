from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from realestate.models import (
    User,
    Apartment,
    ApartmentImage,
    PaymentPlan,
    Contract,
    PaymentSchedule,
)


class Command(BaseCommand):
    help = "HomeMarket uchun admin rollari va permissionlarni yaratadi"

    def handle(self, *args, **options):

        roles = {
            "Manager": {
                Apartment: ["view", "add", "change"],
                ApartmentImage: ["view", "add", "change", "delete"],
                User: ["view", "change"],
                Contract: ["view", "add", "change"],
                PaymentPlan: ["view"],
                PaymentSchedule: ["view"],
            },

            "Sales": {
                Apartment: ["view"],
                ApartmentImage: ["view"],
                User: ["view", "add", "change"],
                Contract: ["view", "add", "change"],
                PaymentPlan: ["view"],
                PaymentSchedule: ["view"],
            },

            "Accountant": {
                User: ["view"],
                Apartment: ["view"],
                Contract: ["view"],
                PaymentPlan: ["view", "add", "change"],
                PaymentSchedule: ["view", "add", "change", "delete"],
            },

            "Content Manager": {
                Apartment: ["view", "add", "change"],
                ApartmentImage: ["view", "add", "change", "delete"],
            },
        }

        for role_name, model_permissions in roles.items():

            group, created = Group.objects.get_or_create(
                name=role_name
            )

            # Eski permissionlarni tozalaymiz.
            # Command qayta ishga tushirilganda
            # permissionlar takrorlanib ketmaydi.
            group.permissions.clear()

            for model, actions in model_permissions.items():

                content_type = ContentType.objects.get_for_model(model)

                for action in actions:

                    permission_codename = (
                        f"{action}_{model._meta.model_name}"
                    )

                    try:
                        permission = Permission.objects.get(
                            content_type=content_type,
                            codename=permission_codename,
                        )

                    except Permission.DoesNotExist:

                        self.stdout.write(
                            self.style.WARNING(
                                f"Permission topilmadi: "
                                f"{permission_codename}"
                            )
                        )

                        continue

                    group.permissions.add(permission)

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Role yaratildi: {role_name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Role yangilandi: {role_name}"
                    )
                )

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "HomeMarket rollari muvaffaqiyatli sozlandi."
            )
        )