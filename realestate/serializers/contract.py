from realestate.serializers.apartment import ApartmentListSerializer
from realestate.models import Apartment, Contract, PaymentPlan
from realestate.services.calculator import calculate_contract_payments
from realestate.services.schedule import generate_payment_schedule
from rest_framework import serializers


class ContractCreateSerializer(serializers.ModelSerializer):
  apartment_id = serializers.IntegerField(write_only=True)
  payment_plan_id = serializers.IntegerField(write_only=True)

  class Meta:
    model = Contract
    fields = [
        'id',
        'apartment_id',
        'payment_plan_id',
        'initial_payment',
        'monthly_payment',
        'remaining_amount',
        'contract_number',
        'status',
    ]
    read_only_fields = [
        'monthly_payment',
        'remaining_amount',
        'contract_number',
        'status',
    ]

  def validate(self, data):
    apartment_id = data.get('apartment_id')
    payment_plan_id = data.get('payment_plan_id')
    initial_payment = data.get('initial_payment')

    try:
      apartment = Apartment.objects.get(
          id=apartment_id, status='available'
      )
    except Apartment.DoesNotExist:
      raise serializers.ValidationError(
          {'apartment_id': 'Bunday kvartira topilmadi yoki allaqachon band qilingan.'}
      )

    try:
      payment_plan = PaymentPlan.objects.get(id=payment_plan_id, is_active=True)
    except PaymentPlan.DoesNotExist:
      raise serializers.ValidationError(
          {'payment_plan_id': 'Bunday to‘lov sharti mavjud emas.'}
      )

    min_initial = (
        apartment.total_price * payment_plan.min_initial_payment_percent
    ) / 100
    if initial_payment < min_initial:
      raise serializers.ValidationError({
          'initial_payment': (
              f"Boshlang'ich to'lov kamida {min_initial} so'm"
              f" ({payment_plan.min_initial_payment_percent}%) bo'lishi kerak."
          )
      })

    try:
      calc_result = calculate_contract_payments(
          total_price=apartment.total_price,
          initial_payment=initial_payment,
          duration_months=payment_plan.duration_months,
      )
    except ValueError as e:
      raise serializers.ValidationError({'non_field_errors': str(e)})

    data['apartment'] = apartment
    data['payment_plan'] = payment_plan
    data['calculated_data'] = calc_result
    return data

  def create(self, validated_data):
    apartment = validated_data.pop('apartment')
    payment_plan = validated_data.pop('payment_plan')
    calc_result = validated_data.pop('calculated_data')
    validated_data.pop('apartment_id')
    validated_data.pop('payment_plan_id')

    user = self.context['request'].user
    import time

    contract_number = f'CON-{int(time.time())}'

    contract = Contract.objects.create(
        client=user,
        apartment=apartment,
        payment_plan=payment_plan,
        initial_payment=validated_data['initial_payment'],
        monthly_payment=calc_result['monthly_payment'],
        remaining_amount=calc_result['remaining_amount'],
        contract_number=contract_number,
        status='pending',
    )
    generate_payment_schedule(contract)


    apartment.status = 'reserved'
    apartment.save()

    return contract


# ANASHU QISM TO'G'RI YOZILGANIDAN ISHONCH HOSIL QILING:
class ContractListSerializer(serializers.ModelSerializer):
  apartment = ApartmentListSerializer(read_only=True)

  class Meta:
    model = Contract
    fields = [
        'id',
        'apartment',
        'initial_payment',
        'monthly_payment',
        'remaining_amount',
        'contract_number',
        'created_at',
        'status',
    ]