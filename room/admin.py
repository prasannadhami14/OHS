from django.contrib import admin
from .models import Room
@admin.register(Room)
# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    list_display=['id','hotel','image','room_type','room_number','description','price','availabilityStatus']
