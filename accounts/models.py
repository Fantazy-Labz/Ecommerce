from django.db import models

# Create your models here.
class CustomUser(models.Model):

    phone_number = models.CharField(max_length=20, blank=True, null=True) 
    adress= models.CharField(max_length=100, blank=True, null=True)
    is_email_verified = models.BooleanField()

    def __str__(self):
        return self.email

class Profile(models.Model):

    user = models.CharField(max_length=30, unique=True)
    bio = models.TextField(max_length=300)
    picture = models.ImageField()

    def __str__(self):
        return self.user

    