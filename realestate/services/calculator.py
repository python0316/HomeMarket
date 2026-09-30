from decimal import Decimal


def calculate_contract_payments(
    total_price: Decimal, initial_payment: Decimal, duration_months: int
):
  """Kvartira narxi, boshlang'ich to'lov va muddat bo'yicha

  qolgan summa hamda oylik to'lovni hisoblab beruvchi funksiya.
  """
  if initial_payment >= total_price:
    raise ValueError(
        "Boshlang'ich to'lov uyning umumiy narxidan ko'p yoki teng bo'lishi"
        " mumkin emas."
    )

  if duration_months <= 0:
    raise ValueError("Muddat (oylar soni) 0 dan katta bo'lishi kerak.")

  # Qolgan summa
  remaining_amount = total_price - initial_payment

  # Oylik to'lovni oddiy taqsimlash (agar foizsiz bo'lsa)
  monthly_payment = remaining_amount / Decimal(duration_months)

  # Natijalarni 2 xona aniqlikda yaxlitlaymiz
  return {
      "remaining_amount": round(remaining_amount, 2),
      "monthly_payment": round(monthly_payment, 2),
  }