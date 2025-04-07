from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def viewProducts():
    products = Product.objects.all()
    return JsonResponse({
        "status": "success",
        "products": products})

@csrf_exempt
def viewDetails(product_id):
    product = get_object_or_404(Product, id = product_id)
    return JsonResponse({
        "status": "success",
        "product": {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock
        }
    })

@csrf_exempt
def addProduct(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product = Product.objects.create(
                name=data['name'],
                description=data['description'],
                price=data['price'],
                stock=data['stock']
            )
            return JsonResponse({'status': 'success', 'product_id': product.id})
        except KeyError as e:   
            return JsonResponse({'status': 'error', 'message': f'Missing field: {str(e)}'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def updateProduct():
    # Logic to update a product
    pass

@csrf_exempt
def deleteProduct(product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return JsonResponse({'status': 'success', 'message': 'Product deleted successfully'})
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)