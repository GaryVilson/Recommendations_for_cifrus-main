from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'), # http://127.0.0.1:8000
    path('product/<int:product_id>', product, name='product'), # http://127.0.0.1:8000/product/
    path('category/<int:subcategory_id>', category, name='category') # http://127.0.0.1:8000/category/
]
