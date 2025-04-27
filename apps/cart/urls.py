# apps/cart/urls.py

from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('detail/', views.CartDetailView.get, name='detail'),
    path('add/<int:product_id>/', views.AddToCartView.post, name='add'),
    path('update/<int:item_id>/', views.UpdateCartView.post, name='update'),
    path('remove/<int:item_id>/', views.RemoveFromCartView.post, name='remove'),
    path('checkout/', views.CheckoutView.get, name='checkout'),
]