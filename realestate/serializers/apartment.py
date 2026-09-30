from rest_framework import serializers
from realestate.models import Apartment


class ApartmentListSerializer(serializers.ModelSerializer):

  class Meta:
    model = Apartment
    fields = [
        'id',
        'room_count',
        'square_meters',
        'floor',
        'total_price',
        'status',
        'model_3d_file',
        'description',
    ]