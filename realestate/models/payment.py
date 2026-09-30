from django.db import models
from .user import User
from .apartment import Apartment


class PaymentPlan(models.Model):
  duration_months = models.IntegerField()
  min_initial_payment_percent = models.DecimalField(
      max_digits=5, decimal_places=2, default=30.0
  )
  interest_rate = models.DecimalField(
      max_digits=5, decimal_places=2, default=0.0
  )
  is_active = models.BooleanField(default=True)

  def __str__(self):
    return (
        f"{self.duration_months} oyga (Min. boshlang'ich:"
        f" {self.min_initial_payment_percent}%)"
    )


class Contract(models.Model):
  STATUS_CHOICES = (
      ("pending", "Kutilmoqda / Ko‘rib chiqilmoqda"),
      ("approved", "Tasdiqlangan"),
      ("cancelled", "Bekor qilingan"),
  )

  client = models.ForeignKey(
      User, on_delete=models.CASCADE, limit_choices_to={"is_client": True}
  )
  apartment = models.ForeignKey(Apartment, on_delete=models.PROTECT)
  payment_plan = models.ForeignKey(PaymentPlan, on_delete=models.PROTECT)

  initial_payment = models.DecimalField(max_digits=12, decimal_places=2)
  monthly_payment = models.DecimalField(max_digits=12, decimal_places=2)
  remaining_amount = models.DecimalField(max_digits=12, decimal_places=2)

  contract_number = models.CharField(max_length=50, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)
  status = models.CharField(
      max_length=20, choices=STATUS_CHOICES, default="pending"
  )

  def __str__(self):
    return f"Shartnoma № {self.contract_number} - {self.client.username}"


class PaymentSchedule(models.Model):
  STATUS_CHOICES = [
      ('pending', 'Kutilmoqda'),
      ('paid', "To'langan"),
      ('overdue', "Muddati o'tgan"),
  ]

  contract = models.ForeignKey(
      Contract, on_delete=models.CASCADE, related_name='payment_schedules'
  )
  month_number = models.IntegerField(
      help_text="Nechanchi oy ekanligi (1, 2, 3...)"
  )
  amount = models.DecimalField(max_digits=12, decimal_places=2)
  due_date = models.DateField(help_text="To'lov qilinishi kerak bo'lgan sana")
  status = models.CharField(
      max_length=20, choices=STATUS_CHOICES, default='pending'
  )  # <-- max_digits olib tashlandi
  paid_at = models.DateTimeField(null=True, blank=True)

  def __str__(self):
    return (
        f"Shartnoma #{self.contract.contract_number} -"
        f" {self.month_number}-oy ({self.amount})"
    )