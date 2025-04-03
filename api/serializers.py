from rest_framework import serializers
from .models import Category, Product, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['slug', 'name', 'url']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['url']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'discount_percentage',
            'rating', 'stock', 'category', 'thumbnail', 'images'
        ]

class ProductsResponseSerializer(serializers.Serializer):
    limit = serializers.IntegerField()
    skip = serializers.IntegerField()
    total = serializers.IntegerField()
    products = ProductSerializer(many=True)