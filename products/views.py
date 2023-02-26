from django.http import HttpResponse
from django.shortcuts import render
from .models import Product, Category
from django.template import loader

# Create your views here.


def show_products(request, category_name=None):
    """Show all products"""
    products = Product.objects.all()
    categories = Category.objects.all()

    if category_name:
        category = Category.objects.get(name=category_name)
        title = category.name
        products = products.filter(category=category)
    else:
        title = "Main"

    template = loader.get_template('products/show_products.html')
    context = {'products': products, 'categories': categories, 'title': title}

    return HttpResponse(template.render(context, request))

def show_product(request, slug):
    """Returns a product that user have chosen"""
    product = Product.objects.get(slug=slug)
    template = loader.get_template('products/product_details.html')
    context = {'product': product}
    return HttpResponse(template.render(context,request))

