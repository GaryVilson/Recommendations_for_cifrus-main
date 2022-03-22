import random
import numpy as np


from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from .models import *
from scripts.recommendations import run


def get_categories():
    categories = {}
    for category in Category.objects.all():
        subcategories = [[subcategory.id, subcategory.name] for subcategory in
                         Subcategory.objects.filter(category=category.id)]
        categories[category.name] = subcategories
    return categories


def index(request):
    products = Products.objects.all()
    random_products = []
    while len(random_products) < 16:
        random_product = random.choice(products)
        if random_product not in random_products:
            random_products.append(random_product)
    return render(request, 'main/index.html', context={'categories': get_categories(),
                                                       'random_products': random_products})


def category(request, subcategory_id):
    print(subcategory_id)
    products = Products.objects.filter(subcategory=subcategory_id)
    print(products)
    return render(request, 'main/category.html', context={'categories': get_categories(),
                                                          'products': products})


def product(request, product_id):
    product = Products.objects.get(id=product_id)

    recommended_products_ids = run(product)
    recommended_products = [Products.objects.get(id=product_id) for product_id in recommended_products_ids]
    specs = {}
    for i in range(0, len(product.specifications)-1, 2):
        specs[product.specifications[i]] = product.specifications[i+1]
    product.specifications = specs
    return render(request, 'main/product.html', context={'categories': get_categories(),
                                                         'product': product,
                                                         'recommended_products': recommended_products})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
