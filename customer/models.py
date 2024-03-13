from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    contactNumber = models.CharField(max_length=15)
    address = models.TextField()
    def __str__(self):
        return f"{self.name}"

# Create your models here.
