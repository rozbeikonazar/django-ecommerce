from django.http import HttpResponse
from django.shortcuts import render
from .models import Product, Category
from django.template import loader
from django.db.models import Q


def show_products(request, category_name=None):
    """Returns all products"""
    products = Product.objects.all()
    categories = Category.objects.all()
    title = 'Main'
    if category_name:
        category = Category.objects.get(name=category_name)
        title = category.name
        products = products.filter(category=category)


    template = loader.get_template('products/show_products.html')
    context = {'products': products, 'categories': categories, 'title': title}

    return HttpResponse(template.render(context, request))

def show_product(request, slug):
    """Returns a product that user have chosen"""
    product = Product.objects.get(slug=slug)
    title = product.name
    template = loader.get_template('products/product_details.html')
    context = {'product': product, 'title': title}
    return HttpResponse(template.render(context,request))



def search_products(request):
    """Returns all products that were specified by query"""
    if request.method == "POST":
        query = request.POST.get('searched')
        if query:
            products = Product.objects.filter(
                Q(name__contains=query) |
                Q(description__contains=query) |
                Q(category__name__contains=query)
            )
            categories = Category.objects.all()
            return render(request, 'products/search_products.html', {'searched': query, 'products': products, 'categories': categories})
    return render(request, 'products/search_products.html')

