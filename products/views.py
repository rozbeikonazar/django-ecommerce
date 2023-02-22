from django.http import HttpResponse
from django.shortcuts import render
from .models import Product, Category
from django.template import loader

# Create your views here.


def show_products(request, category_name=None):
    products = Product.objects.all()
    categories = Category.objects.all()
    if category_name:
        products = Product.objects.filter(category__name=category_name) 
    template = loader.get_template('products/show_products.html')
    context = {'products': products, 'categories': categories}

    return HttpResponse(template.render(context, request))



def show_product(request, id):
    product = Product.objects.get(id=id)
    template = loader.get_template('products/product_details.html')
    context = {'product': product}
    return HttpResponse(template.render(context,request))

