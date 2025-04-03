from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.get_products_list, name='products-list'),
    path('products/search/', views.search_products, name='products-search'),
    path('products/<int:id>/', views.get_single_product, name='single-product'),
    path('products/categories/', views.get_all_categories, name='categories-list'),
    path('products/category/<str:category_name>/', views.get_products_by_category, name='products-by-category'),
]