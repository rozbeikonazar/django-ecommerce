from django.conf import settings
from products.models import Category
from django.core.cache import cache

def categories_processor(request):
    categories_cache = cache.get(settings.CATEGORIES_CACHE)
    if categories_cache:
        categories = categories_cache
    else:
        categories = Category.objects.all()
        cache.set(settings.CATEGORIES_CACHE, categories, 60*60*24)
    
    return {'categories': categories}