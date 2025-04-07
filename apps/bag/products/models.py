from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model): 

    OPTIONS = [
        ("ELECTRONICA", "Electronica"),
        ("ENTRETENIMIENTO", "Entretenimiento"),
        ("BIENESTAR", "Bienestar"),
        ("OTROS", "Otros")
    ]

    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=250)  # Fixed typo
    price = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100000)])
    category = models.CharField(max_length=30, choices = OPTIONS)
    stock = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    image = models.ImageField(upload_to='product_pic', default='defaulr.png')

    def __str__(self):
        return self.name
    