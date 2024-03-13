from django.contrib import admin
from .models import Customer
admin.site.site_header = "Hotel Reservation"
admin.site.site_title = "Your Admin Portal"
admin.site.index_title = "Welcome to Our System"
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # title=['customerID','name','email','contactNumber','address']
    list_display=['name','email','contactNumber','address']