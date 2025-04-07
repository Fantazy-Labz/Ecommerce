# apps/cart/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from products.models import Product
from .models import Cart, CartItem
from .cart import CartManager

def cart_detail(request):
    """
    Muestra el contenido detallado del carrito
    """
    cart_manager = CartManager(request)
    cart = cart_manager.get_cart()
    
    return render(request, 'cart/detail.html', {
        'cart': cart,
        'items': cart_manager.get_items()
    })

@require_POST
def add_to_cart(request, product_id):
    """
    Añade un producto al carrito
    """
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    cart_manager = CartManager(request)
    cart_manager.add(product, quantity)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Solicitud AJAX
        return JsonResponse({
            'status': 'success',
            'message': f'{product.name} añadido al carrito',
            'cart_total': cart_manager.get_total_items(),
            'cart_price': cart_manager.get_total_price()
        })
    
    messages.success(request, f'{product.name} añadido al carrito')
    return redirect('cart:detail')

@require_POST
def update_cart(request, item_id):
    """
    Actualiza la cantidad de un elemento del carrito
    """
    quantity = int(request.POST.get('quantity', 1))
    
    cart_manager = CartManager(request)
    cart_manager.update(item_id, quantity)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'cart_total': cart_manager.get_total_items(),
            'cart_price': cart_manager.get_total_price()
        })
    
    return redirect('cart:detail')

@require_POST
def remove_from_cart(request, item_id):
    """
    Elimina un elemento del carrito
    """
    cart_manager = CartManager(request)
    product_name = cart_manager.remove(item_id)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': f'{product_name} eliminado del carrito',
            'cart_total': cart_manager.get_total_items(),
            'cart_price': cart_manager.get_total_price()
        })
    
    messages.success(request, f'{product_name} eliminado del carrito')
    return redirect('cart:detail')

@login_required
def checkout(request):
    """
    Página de finalización de compra
    """
    cart_manager = CartManager(request)
    cart = cart_manager.get_cart()
    items = cart_manager.get_items()
    
    if not items:
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('cart:detail')
    
    # Aquí puedes recuperar la información de envío del usuario si la tienes
    
    return render(request, 'cart/checkout.html', {
        'cart': cart,
        'items': items
    })