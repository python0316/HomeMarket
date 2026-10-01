from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from realestate.audit_context import (
    get_current_user,
    get_current_ip,
)

from realestate.models import (
    User,
    Apartment,
    ApartmentImage,
    Contract,
    PaymentPlan,
    PaymentSchedule,
    AuditLog,
)


# =========================================================
# Yordamchi funksiya
# =========================================================

def create_audit_log(
    *,
    action,
    instance,
    description='',
):
    """
    AuditLog yaratish uchun umumiy funksiya.
    """

    user = get_current_user()
    ip_address = get_current_ip()

    AuditLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action=action,
        model_name=instance.__class__.__name__,
        object_id=str(instance.pk),
        description=description,
        ip_address=ip_address,
    )


# =========================================================
# User
# =========================================================

@receiver(post_save, sender=User)
def user_saved(sender, instance, created, **kwargs):
    action = 'create' if created else 'update'

    create_audit_log(
        action=action,
        instance=instance,
        description=(
            f"User '{instance.username}' "
            f"{'yaratildi' if created else 'o‘zgartirildi'}."
        ),
    )


@receiver(post_delete, sender=User)
def user_deleted(sender, instance, **kwargs):
    create_audit_log(
        action='delete',
        instance=instance,
        description=(
            f"User '{instance.username}' o‘chirildi."
        ),
    )


# =========================================================
# Apartment
# =========================================================

@receiver(post_save, sender=Apartment)
def apartment_saved(sender, instance, created, **kwargs):
    action = 'create' if created else 'update'

    create_audit_log(
        action=action,
        instance=instance,
        description=(
            f"Apartment '{instance.title or instance.pk}' "
            f"{'yaratildi' if created else 'o‘zgartirildi'}."
        ),
    )


@receiver(post_delete, sender=Apartment)
def apartment_deleted(sender, instance, **kwargs):
    create_audit_log(
        action='delete',
        instance=instance,
        description=(
            f"Apartment '{instance.title or instance.pk}' "
            f"o‘chirildi."
        ),
    )


# =========================================================
# ApartmentImage
# =========================================================

@receiver(post_save, sender=ApartmentImage)
def apartment_image_saved(sender, instance, created, **kwargs):
    action = 'create' if created else 'update'

    create_audit_log(
        action=action,
        instance=instance,
        description=(
            f"Apartment rasmi "
            f"{'qo‘shildi' if created else 'o‘zgartirildi'}."
        ),
    )


@receiver(post_delete, sender=ApartmentImage)
def apartment_image_deleted(sender, instance, **kwargs):
    create_audit_log(
        action='delete',
        instance=instance,
        description='Apartment rasmi o‘chirildi.',
    )


# =========================================================
# PaymentPlan
# =========================================================

@receiver(post_save, sender=PaymentPlan)
def payment_plan_saved(sender, instance, created, **kwargs):
    action = 'create' if created else 'update'

    create_audit_log(
        action=action,
        instance=instance,
        description=(
            f"PaymentPlan "
            f"{'yaratildi' if created else 'o‘zgartirildi'}."
        ),
    )


@receiver(post_delete, sender=PaymentPlan)
def payment_plan_deleted(sender, instance, **kwargs):
    create_audit_log(
        action='delete',
        instance=instance,
        description='PaymentPlan o‘chirildi.',
    )


# =========================================================
# Contract
# =========================================================

@receiver(post_save, sender=Contract)
def contract_saved(sender, instance, created, **kwargs):
    action = 'create' if created else 'update'

    create_audit_log(
        action=action,
        instance=instance,
        description=(
            f"Contract "
            f"{'yaratildi' if created else 'o‘zgartirildi'}."
        ),
    )


@receiver(post_delete, sender=Contract)
def contract_deleted(sender, instance, **kwargs):
    create_audit_log(
        action='delete',
        instance=instance,
        description='Contract o‘chirildi.',
    )


# =========================================================
# PaymentSchedule
# =========================================================

@receiver(post_save, sender=PaymentSchedule)
def payment_schedule_saved(
    sender,
    instance,
    created,
    **kwargs,
):
    action = 'create' if created else 'update'

    create_audit_log(
        action=action,
        instance=instance,
        description=(
            f"PaymentSchedule "
            f"{'yaratildi' if created else 'o‘zgartirildi'}."
        ),
    )


@receiver(post_delete, sender=PaymentSchedule)
def payment_schedule_deleted(
    sender,
    instance,
    **kwargs,
):
    create_audit_log(
        action='delete',
        instance=instance,
        description='PaymentSchedule o‘chirildi.',
    )