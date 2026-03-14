from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Case, When, IntegerField
from django.core.paginator import Paginator
from django.core.cache import cache
from urllib.parse import urlencode

from .models import Product
from recommendations.services.recommender import RecommenderService

_recommender_service = None

def get_recommender_service():
    global _recommender_service
    if _recommender_service is None:
        _recommender_service = RecommenderService()
    return _recommender_service


def _clean_categories():
    """Clean and extract main categories from products with caching."""
    cache_key = 'cleaned_categories'
    categories = cache.get(cache_key)
    if categories is None:
        raw_categories = Product.objects.values_list("category", flat=True).distinct()
        cleaned_categories = set()
        for cat in raw_categories:
            if cat:
                main_cat = cat.split(">")[0].strip()
                cleaned_categories.add(main_cat)
        categories = sorted(cleaned_categories)
        cache.set(cache_key, categories, 3600)  # Cache for 1 hour
    return categories


def product_list_view(request):

    products = Product.objects.all()

    # Remove products without price
    products = products.exclude(price__isnull=True)

    # SEARCH
    search_query = request.GET.get("search")
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(brand__icontains=search_query)
        )

    # CATEGORY FILTER
    selected_category = request.GET.get("category")
    if selected_category:
        products = products.filter(category__icontains=selected_category)

    # PRICE FILTER
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if min_price:
        try:
            min_price = float(min_price)
            if min_price >= 0:
                products = products.filter(price__gte=min_price)
        except ValueError:
            pass  # Ignore invalid input

    if max_price:
        try:
            max_price = float(max_price)
            if max_price >= 0:
                products = products.filter(price__lte=max_price)
        except ValueError:
            pass  # Ignore invalid input

    # PRIORITIZE PRODUCTS WITH IMAGES
    products = products.annotate(
        has_image=Case(
            When(image_url__isnull=False, then=1),
            default=0,
            output_field=IntegerField(),
        )
    )

    # SORTING
    sort = request.GET.get("sort")

    if sort == "price_low":
        products = products.order_by("-has_image", "price")
    elif sort == "price_high":
        products = products.order_by("-has_image", "-price")
    elif sort == "rating":
        products = products.order_by("-has_image", "-rating")
    else:
        products = products.order_by("-has_image", "-created_at")

    # ----------------------------
    # PAGINATION (INDUSTRY LEVEL)
    # ----------------------------
    paginator = Paginator(products, 12)  # 12 products per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Preserve existing query parameters except 'page'
    query_params = request.GET.copy()
    query_params.pop("page", None)
    query_string = urlencode(query_params)

    # CLEAN SIDEBAR CATEGORIES
    categories = _clean_categories()

    return render(request, "products/product_list.html", {
        "page_obj": page_obj,
        "categories": categories,
        "selected_category": selected_category,
        "query_string": query_string,
    })


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    recommendations = get_recommender_service().get_recommendations(
        product.name,
        top_n=4
    )

    return render(request, "products/product_detail.html", {
        "product": product,
        "recommendations": recommendations,
        "quantity_range": range(1, 6),  
    })