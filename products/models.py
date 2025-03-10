from django.db import models
from django import validators

# Create your models here.
class Product(model.Models):
    name = models.CharField(max_length=30, unique=True)
    desciption = models.TextField(max_length=250)
    price = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100000)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.name

class Categorie(model.Models):
    name = models.CharField(max_length=30, unique=True)
    desciption = models.TextField(max_length=250)
    
    def __str__(self):
        return self.name