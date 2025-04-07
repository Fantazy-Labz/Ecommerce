from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
#from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .serializers import ProductSerializer
from .models import Product

@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def productDetails(request, product_id):
    product = Product.objects.get(id=product_id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['POST'])
#@permission_classes([IsAdminUser])
def addProduct(request):
    """
    Crea un nuevo producto.
    """
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status': 'success',
            'product_id': serializer.data['id'],
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'status': 'error',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
#@permission_classes([IsAdminUser])
def updateProduct(request, product_id):
    """
    Actualiza un producto existente.
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Producto no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # PUT para actualización completa, PATCH para actualización parcial
    partial = request.method == 'PATCH'
    serializer = ProductSerializer(product, data=request.data, partial=partial)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status': 'success',
            'product_id': serializer.data['id'],
            'data': serializer.data
        })
    return Response({
        'status': 'error',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
#@permission_classes([IsAdminUser])
def deleteProduct(request, product_id):
    """
    Elimina un producto.
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Producto no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    
    product_name = product.name 
    product.delete()
    return Response({
        'status': 'success',
        'message': f'Producto "{product_name}" eliminado correctamente'
    })