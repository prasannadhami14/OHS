from django.db import models
from django.core.validators import MinValueValidator

class RoomType(models.Model):
    name = models.CharField(max_length=255,default=None)
    description = models.TextField(max_length=255)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])  # Ensure capacity is at least 1
    amenities = models.TextField(max_length=255)
    # displying room type name in string format
    def __str__(self):
        return f"{self.name}"
       
