# cart/models.py
from django.db import models
from .models import CustomUser
from products.models import Product
from django.core.validators import MinValueValidator

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    session_id = models.CharField(max_length=100, null=True, blank=True)  # For anonymous users
    
    def __str__(self):
        return f"Cart {self.id}"
    
    @property
    def total(self):
        items = self.cartitem_set.all()
        return sum([item.subtotal for item in items])

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    
    @property
    def subtotal(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"    