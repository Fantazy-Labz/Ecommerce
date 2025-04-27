# apps/cart/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404

from products.models import Product
from .models import Cart, CartItem
from .cart import CartManager
from .serializers import CartSerializer, CartItemSerializer


class CartDetailView(APIView):
    """
    Muestra el contenido detallado del carrito
    """
    def get(self, request):
        cart_manager = CartManager(request)
        cart = cart_manager.get_cart()
        items = cart_manager.get_items()
        
        # Serializa los datos para la respuesta
        serializer = CartSerializer(cart)
        items_serializer = CartItemSerializer(items, many=True)
        
        return Response({
            'cart': serializer.data,
            'items': items_serializer.data
        })


class AddToCartView(APIView):
    """
    Añade un producto al carrito
    """
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.data.get('quantity', 1))
        
        cart_manager = CartManager(request)
        cart_manager.add(product, quantity)
        
        return Response({
            'status': 'success',
            'message': f'{product.name} añadido al carrito',
            'cart_total': cart_manager.get_total_items(),
            'cart_price': cart_manager.get_total_price()
        }, status=status.HTTP_201_CREATED)


class UpdateCartView(APIView):
    """
    Actualiza la cantidad de un elemento del carrito
    """
    def post(self, request, item_id):
        quantity = int(request.data.get('quantity', 1))
        
        cart_manager = CartManager(request)
        cart_manager.update(item_id, quantity)
        
        return Response({
            'status': 'success',
            'cart_total': cart_manager.get_total_items(),
            'cart_price': cart_manager.get_total_price()
        })


class RemoveFromCartView(APIView):
    """
    Elimina un elemento del carrito
    """
    def post(self, request, item_id):
        cart_manager = CartManager(request)
        product_name = cart_manager.remove(item_id)
        
        return Response({
            'status': 'success',
            'message': f'{product_name} eliminado del carrito',
            'cart_total': cart_manager.get_total_items(),
            'cart_price': cart_manager.get_total_price()
        })


class CheckoutView(APIView):
    """
    Página de finalización de compra
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        cart_manager = CartManager(request)
        cart = cart_manager.get_cart()
        items = cart_manager.get_items()
        
        if not items:
            return Response({
                'status': 'error',
                'message': 'Tu carrito está vacío'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Serializa los datos para la respuesta
        serializer = CartSerializer(cart)
        items_serializer = CartItemSerializer(items, many=True)
        
        return Response({
            'cart': serializer.data,
            'items': items_serializer.data
        })