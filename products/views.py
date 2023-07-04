from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.paginator import Paginator

def get_products_from_cache(cache_key):
    """
    Retrieves product IDs from cache
    """
    product_ids = cache.get(cache_key)
    if product_ids:
        return Product.objects.filter(id__in=product_ids)

def get_products_from_db(cache_key, queryset=None):
    if queryset is None:
            queryset = Product.objects.all()
    products = queryset
    product_ids = list(products.values_list('id', flat=True))
    cache.set(cache_key, product_ids, 60*60*24)
    return products

def get_cached_products(cache_key, queryset=None):
    """
    Retrieves products from the cache or database
    """
    products = get_products_from_cache(cache_key)
    if not products:
        products = get_products_from_db(cache_key, queryset)

    return products

def get_paginated_products(request, products):
    """
    Returns a paginated list of products
    """
    paginator = Paginator(products, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj

def show_products(request):
    """
    Returns all products
    """
    title = 'Main'
    products_cache_key = settings.PRODUCTS_CACHE
    products = get_cached_products(products_cache_key)
    page_obj = get_paginated_products(request, products)
    context = {'title': title, "page_obj": page_obj}
    return render(request, 'products/show_products.html', context)

def show_products_by_category(request, category_name):
    """
    Returns all products specified by category
    """
    category = get_object_or_404(Category, name=category_name)
    products_cache_key = f"products_{category_name}"
    products = get_cached_products(products_cache_key, Product.objects.select_related('category').filter(category=category))
    page_obj = get_paginated_products(request, products)
    context = {"page_obj": page_obj, 'title': category_name}
    return render(request, 'products/show_products.html', context)

@cache_page(60*15)
def show_product(request, slug):
    """
    Returns a product that user have chosen
    """
    product = get_object_or_404(Product, slug=slug)
    title = product.name

    context = {'product': product, 'title': title}
    return render(request, 'products/product_details.html', context)

def search_products(request):
    """
    Returns all products that were specified by query
    """
    if request.method == "POST":
        query = request.POST.get('searched')
        if query:
            products_cache_key = f'search_products_{query}'
            products = get_cached_products(products_cache_key,
                Product.objects.filter(
                    Q(name__icontains=query) |
                    Q(description__icontains=query) |
                    Q(category__name__icontains=query)
                )
            )
            page_obj = get_paginated_products(request, products)
            context = {'searched': query, 'page_obj': page_obj}
            return render(request, 'products/search_products.html', context)
    context = {'page_obj': None}
    return render(request, 'products/search_products.html', context)


def change_products_quantity(items):
    for item in items:
        product = item.product
        product.quantity -= item.quantity
        product.save()