from django.shortcuts import get_object_or_404, render
from .models import Product

# Create your views here.
def view_products(request):
    products = Product.objects.all()
    return render(request, "dashboard.html", {"products": products})


def view_details(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    name = product.name
    description= product.description
    category= product.category
    stock= product.stock
    price= product.price
    return render(request, "product_details.html" , {"product": product, "name":name, "description": description, "category": category, "stock": stock, "price": price})
