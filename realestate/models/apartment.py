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

  room_count = models.IntegerField(choices=ROOM_CHOICES)
  square_meters = models.DecimalField(max_digits=6, decimal_places=2)
  floor = models.IntegerField()
  total_price = models.DecimalField(max_digits=12, decimal_places=2)
  status = models.CharField(
      max_length=20, choices=STATUS_CHOICES, default="available"
  )
  model_3d_file = models.FileField(
      upload_to="apartments/3d/", blank=True, null=True
  )
  description = models.TextField(blank=True, null=True)

  def __str__(self):
    return (
        f"{self.room_count}-xona, {self.square_meters} m² - {self.total_price}"
        " so'm"
    )