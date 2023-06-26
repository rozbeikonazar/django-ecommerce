from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.conf import settings

def get_cached_products(cache_key, queryset=None):
    """
    Retrieves products from the cache or database.
    """
    product_ids = cache.get(cache_key)
    if product_ids:
        products = Product.objects.filter(id__in=product_ids)
    else:
        if queryset is None:
            queryset = Product.objects.all()
        products = queryset
        product_ids = list(products.values_list('id', flat=True))
        cache.set(cache_key, product_ids, 60*60*24)
    return products

def show_products(request):
    """
    Returns all products
    """
    title = 'Main'
    cache_key = settings.PRODUCTS_CACHE
    products = get_cached_products(cache_key)

    context = {'products': products, 'title': title}
    return render(request, 'products/show_products.html', context)

def show_products_by_category(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    cache_key = f"products_{category_name}"
    products = get_cached_products(cache_key, Product.objects.filter(category=category))

    context = {'products': products, 'title': category_name}
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
            cache_key = f'search_products_{query}'
            products = get_cached_products(cache_key,
                Product.objects.filter(
                    Q(name__icontains=query) |
                    Q(description__icontains=query) |
                    Q(category__name__icontains=query)
                )
            )
            return render(request, 'products/search_products.html', {'searched': query, 'products': products})
    return render(request, 'products/search_products.html')
