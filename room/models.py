from django.db import models
from hotel.models import Hotel
from room_type.models import RoomType

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='media/',blank=True)
    room_type =  models.ForeignKey(RoomType,on_delete=models.CASCADE, default=None)  # Assuming RoomType model exists
    # room_number =models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10,default=None) # Room number
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availabilityStatus = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.room_type}"
