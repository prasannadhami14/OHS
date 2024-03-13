# Create your models here.
from django.db import models
from django.utils import timezone
from room.models import Room
class Booking(models.Model):
    user= models.CharField(max_length=255)
    contact= models.CharField(max_length=10)
    email=models.EmailField(default='None')
    room_type= models.ForeignKey(Room, on_delete=models.CASCADE)
    bookingDate = models.DateTimeField(auto_now_add=True)
    checkInDate = models.DateField()
    checkOutDate = models.DateField()
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancled', 'Cancled'),
    ])

    def __str__(self):
        return f" Room {self.room_type.room_number} - Customer {self.user}"
# for reservation expires
class ReservationCard(models.Model):
    reservation_time = models.DateTimeField()
    expiration_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=(('pending', 'Pending'), ('confirmed', 'Confirmed'), ('expired', 'Expired'), ('cancelled', 'Cancelled')))

    def __str__(self):
        return f'ReservationCard {self.id}'

    def is_expired(self):
        return self.expiration_time < timezone.now()

    def cancel(self):
        self.status = 'cancelled'
        self.save()