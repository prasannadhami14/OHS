from django.contrib import admin
from .models import RoomType
@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display=['id','name','description','capacity','amenities']