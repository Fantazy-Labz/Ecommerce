# apps/products/serializers.py
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'stock', 'image']
        read_only_fields = ['id']
        
    def validate_price(self, value):
        """
        Validación personalizada para el precio.
        """
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que cero.")
        return value
    
    def validate_stock(self, value):
        """
        Validación personalizada para el stock.
        """
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return value