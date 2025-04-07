# apps/cart/cart.py

from django.conf import settings
from .models import Cart, CartItem
from products.models import Product

class CartManager:
    """
    Gestor del carrito que maneja todas las operaciones relacionadas con el carrito
    """
    def __init__(self, request):
        self.request = request
        self.session = request.session
        
        # Determinar si el usuario está autenticado
        self.user = request.user if request.user.is_authenticated else None
        
        # Obtener o crear la sesión del carrito para usuarios anónimos
        self.session_id = self.session.session_key
        if not self.session_id:
            # Crear una nueva sesión si no existe
            self.session.save()
            self.session_id = self.session.session_key

    def get_cart(self):
        """
        Obtiene o crea un carrito para el usuario actual o sesión
        """
        if self.user:
            cart, created = Cart.objects.get_or_create(user=self.user)
            # Si teníamos un carrito de sesión, transferir los elementos al carrito de usuario
            if self.session_id:
                session_cart = Cart.objects.filter(session_id=self.session_id).first()
                if session_cart:
                    session_items = CartItem.objects.filter(cart=session_cart)
                    for item in session_items:
                        # Comprobar si el producto ya está en el carrito del usuario
                        existing_item = CartItem.objects.filter(cart=cart, product=item.product).first()
                        if existing_item:
                            existing_item.quantity += item.quantity
                            existing_item.save()
                        else:
                            item.cart = cart
                            item.save()
                    session_cart.delete()
        else:
            cart, created = Cart.objects.get_or_create(session_id=self.session_id)
        
        return cart

    def get_items(self):
        """
        Obtiene todos los elementos del carrito
        """
        cart = self.get_cart()
        return CartItem.objects.filter(cart=cart)

    def add(self, product, quantity=1):
        """
        Añade un producto al carrito o incrementa su cantidad
        """
        cart = self.get_cart()
        
        try:
            # Intentar encontrar el producto en el carrito
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            # Crear un nuevo elemento en el carrito
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity,
                user=self.user,
                session_id=None if self.user else self.session_id
            )
        
        return cart_item

    def update(self, item_id, quantity):
        """
        Actualiza la cantidad de un elemento del carrito
        """
        cart = self.get_cart()
        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            if quantity > 0:
                item.quantity = quantity
                item.save()
            else:
                self.remove(item_id)
        except CartItem.DoesNotExist:
            pass
        
        return True

    def remove(self, item_id):
        """
        Elimina un elemento del carrito
        """
        cart = self.get_cart()
        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            product_name = item.product.name
            item.delete()
            return product_name
        except CartItem.DoesNotExist:
            return ""

    def get_total_items(self):
        """
        Obtiene el número total de elementos en el carrito
        """
        cart = self.get_cart()
        return cart.total_items

    def get_total_price(self):
        """
        Obtiene el precio total del carrito
        """
        cart = self.get_cart()
        return cart.total_price

    def clear(self):
        """
        Vacía el carrito
        """
        cart = self.get_cart()
        CartItem.objects.filter(cart=cart).delete()
        return True

    def transfer_anonymous_cart(self):
        """
        Transfiere el carrito anónimo al usuario recién autenticado
        """
        if not self.user or not self.session_id:
            return False
        
        # Buscar carrito anónimo
        anonymous_cart = Cart.objects.filter(session_id=self.session_id).first()
        if not anonymous_cart:
            return False
        
        # Buscar o crear carrito de usuario
        user_cart, created = Cart.objects.get_or_create(user=self.user)
        
        # Transferir elementos
        anonymous_items = CartItem.objects.filter(cart=anonymous_cart)
        for item in anonymous_items:
            existing_item = CartItem.objects.filter(cart=user_cart, product=item.product).first()
            if existing_item:
                existing_item.quantity += item.quantity
                existing_item.save()
            else:
                item.cart = user_cart
                item.user = self.user
                item.session_id = None
                item.save()
        
        # Eliminar carrito anónimo
        anonymous_cart.delete()
        return True