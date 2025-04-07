# apps/products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.getProducts, name="dashboard"),
    path("details/<int:product_id>/", views.productDetails, name="product_details"),
    path("add/", views.addProduct, name="add_product"),
    path("update/<int:product_id>/", views.updateProduct, name="update_product"),
    path("delete/<int:product_id>/", views.deleteProduct, name="delete_product"),
]