from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# MODELS
class Amenity(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
class Comments(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
class Hotel(models.Model):
    name = models.CharField(max_length=50)
    pan_number = models.CharField(max_length=10,unique=True)
    image=models.ImageField(upload_to='media/',blank=True)
    amenities=models.ManyToManyField(Amenity)
    comment=models.ManyToManyField(Comments,blank=True)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    country = models.CharField(max_length=25)
    zipcode = models.CharField(max_length=5)
    locations = models.CharField(max_length=255,default=None)
    price_range = models.FloatField(max_length=255)
    email=models.EmailField(unique=True)
    phone=PhoneNumberField(max_length=13,unique=True,region='NP')
    def __str__(self):
        return f"{self.name}"
    
