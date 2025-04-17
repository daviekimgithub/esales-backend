from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Category, ProductImage
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    ProductsResponseSerializer,
    ProductImageSerializer
)
import json

@api_view(['GET', 'POST'])
@csrf_exempt
def get_products_list(request):
    if request.method == 'GET':
        limit = int(request.GET.get('limit', 10))
        skip = int(request.GET.get('skip', 0))
        
        products = Product.objects.all()
        total = products.count()
        
        paginator = Paginator(products, limit)
        page = paginator.page((skip // limit) + 1)
        products_page = page.object_list
        
        serializer = ProductsResponseSerializer({
            'limit': limit,
            'skip': skip,
            'total': total,
            'products': products_page
        })
        
        return Response(serializer.data)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            category = Category.objects.get(slug=data["category"])
            product = Product.objects.create(
                category=category,
                title=data["title"],
                description=data["description"],
                price=data["price"],
                discount_percentage=data["discount_percentage"],
                rating=data["rating"],
                stock=data["stock"],
                thumbnail=data["thumbnail"]
            )
            return Response({"id": product.id, "message": "Product added successfully."}, status=status.HTTP_201_CREATED)
        except Category.DoesNotExist:
            return Response({"error": "Category does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@csrf_exempt
def get_all_categories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            category, created = Category.objects.get_or_create(
                slug=data["slug"], defaults={"name": data["name"], "url": data["url"]}
            )
            return Response({"id": category.id, "message": "Category added successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def search_products(request):
    query = request.GET.get('q', '')
    limit = int(request.GET.get('limit', 10))
    skip = int(request.GET.get('skip', 0))
    
    products = Product.objects.filter(title__icontains=query)
    total = products.count()
    
    paginator = Paginator(products, limit)
    page = paginator.page((skip // limit) + 1)
    products_page = page.object_list
    
    serializer = ProductsResponseSerializer({
        'limit': limit,
        'skip': skip,
        'total': total,
        'products': products_page
    })
    
    return Response(serializer.data)

@api_view(['GET'])
def get_single_product(request, id):
    try:
        product = Product.objects.get(pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

from django.core.paginator import Paginator, EmptyPage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def get_products_by_category(request, category_name):
    try:
        # Validate and parse query parameters
        try:
            limit = max(1, min(int(request.GET.get('limit', 10)), 100))  # Clamp between 1-100
            skip = max(0, int(request.GET.get('skip', 0)))  # Ensure non-negative
        except ValueError:
            return Response(
                {"error": "Invalid pagination parameters"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get category by slug (more URL-friendly than name)
        category = Category.objects.get(slug__iexact=category_name)
        
        # Optimized query - only get what we need
        products = Product.objects.filter(category=category).select_related('category')
        total = products.count()
        
        # Handle pagination more robustly
        try:
            paginator = Paginator(products, limit)
            page_number = (skip // limit) + 1
            products_page = paginator.page(page_number).object_list
        except EmptyPage:
            products_page = []

        # Serialize with product images
        serializer = ProductsResponseSerializer({
            'limit': limit,
            'skip': skip,
            'total': total,
            'products': products_page
        })
        
        return Response(serializer.data)
    
    except Category.DoesNotExist:
        return Response(
            {"error": f"Category '{category_name}' not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(['POST'])
@csrf_exempt
def upload_product_image(request):
    """Handles adding images to a product"""
    try:
        data = json.loads(request.body)
        product = Product.objects.get(id=data["product"])
        image = ProductImage.objects.create(product=product, url=data["url"])
        serializer = ProductImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Product.DoesNotExist:
        return Response({"error": "Product does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
