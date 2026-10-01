from rest_framework import serializers
from realestate.models import Apartment, ApartmentImage


class ApartmentImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApartmentImage
        fields = [
            'id',
            'image',
            'title',
            'description',
            'is_main',
        ]


class ApartmentListSerializer(serializers.ModelSerializer):

    images = ApartmentImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Apartment
        fields = [
            'id',
            'title',
            'property_type',
            'room_count',
            'square_meters',
            'floor',
            'total_floors',
            'total_price',
            'address',
            'district',
            'city',
            'renovation',
            'building_year',
            'description',
            'status',
            'has_balcony',
            'has_parking',
            'has_elevator',
            'has_furniture',
            'has_air_conditioner',
            'model_3d_file',
            'images',
            'created_at',
            'updated_at',
        ]