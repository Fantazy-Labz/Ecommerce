from django.contrib import admin
from django.urls import include, path
from .import views

urlpatterns = [
    path("dashboard/", views.view_products, name= "dashboard"),
    path("product_details/<int:product_id>/", views.view_details, name = "product_details")
]
