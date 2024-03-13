from django.contrib import admin
from .models import Hotel,Amenity,Comments

# Register your models here.

@admin.register(Amenity)
class Amenityadmin(admin.ModelAdmin):
    list_display=['id','name']
@admin.register(Hotel)
class hotelAdmin(admin.ModelAdmin):
    list_display=['id','name','pan_number','image','locations','city','state','country','zipcode','email','phone','price_range']
    filter_horizontal = ['amenities']  # This will display amenities in a horizontal filter
@admin.register(Comments)
class Commentsadmin(admin.ModelAdmin):
    list_display=['id','name','email','message','created_at']