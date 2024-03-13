from django.contrib import admin
from .models import Booking
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display=['id','user','contact','room_type','bookingDate','checkInDate','checkOutDate','totalPrice','status']
# Register your models here.
