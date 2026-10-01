from django.db import models


class Apartment(models.Model):
    ROOM_CHOICES = (
        (1, "1-xonali"),
        (2, "2-xonali"),
        (3, "3-xonali"),
        (4, "4+ xonali"),
    )

    STATUS_CHOICES = (
        ("available", "Bo‘sh"),
        ("reserved", "Band qilingan"),
        ("sold", "Sotilgan"),
    )

    RENOVATION_CHOICES = (
        ("new", "Yangi ta’mir"),
        ("renovated", "Ta’mirlangan"),
        ("whitebox", "White Box"),
        ("blackbox", "Qora suvoq"),
        ("none", "Ta’mirsiz"),
    )

    PROPERTY_TYPE_CHOICES = (
        ("apartment", "Kvartira"),
        ("penthouse", "Penthouse"),
        ("studio", "Studio"),
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPE_CHOICES,
        default="apartment"
    )

    room_count = models.IntegerField(
        choices=ROOM_CHOICES
    )

    square_meters = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    floor = models.IntegerField()

    total_floors = models.IntegerField(
        blank=True,
        null=True
    )

    total_price = models.DecimalField(
        max_digits=14,
        decimal_places=2
    )

    address = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    district = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=100,
        default="Toshkent"
    )

    renovation = models.CharField(
        max_length=30,
        choices=RENOVATION_CHOICES,
        blank=True,
        null=True
    )

    building_year = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available"
    )

    has_balcony = models.BooleanField(
        default=False
    )

    has_parking = models.BooleanField(
        default=False
    )

    has_elevator = models.BooleanField(
        default=True
    )

    has_furniture = models.BooleanField(
        default=False
    )

    has_air_conditioner = models.BooleanField(
        default=False
    )

    model_3d_file = models.FileField(
        upload_to="apartments/3d/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} — {self.total_price} so'm"


class ApartmentImage(models.Model):
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="apartments/images/"
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    is_main = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-is_main", "id"]

    def __str__(self):
        return f"{self.apartment.title} - image"