from datetime import date
from dateutil.relativedelta import relativedelta

# Modulning o'zidan to'g'ridan-to'g'ri import qilamiz (adashib ketmasligi uchun)
from realestate.models.payment import PaymentSchedule


def generate_payment_schedule(contract):
  """Shartnoma uchun oylik to'lovlar jadvalini avtomatik yaratish"""
  duration_months = contract.payment_plan.duration_months
  monthly_amount = contract.monthly_payment
  start_date = date.today() + relativedelta(months=1)

  schedules = []
  for month in range(1, duration_months + 1):
    due_date = start_date + relativedelta(months=month - 1)

    schedules.append(
        PaymentSchedule(
            contract=contract,
            month_number=month,
            amount=monthly_amount,
            due_date=due_date,
            status='pending',
        )
    )

  PaymentSchedule.objects.bulk_create(schedules)