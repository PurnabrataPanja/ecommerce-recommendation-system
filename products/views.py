from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product
from recommendations.services.recommender import RecommenderService

recommender_service = RecommenderService()


def product_list_view(request):

    products = Product.objects.all()

    # ===============================
    # SEARCH
    # ===============================
    search_query = request.GET.get("search")
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(brand__icontains=search_query)
        )

    # ===============================
    # CATEGORY FILTER
    # ===============================
    selected_category = request.GET.get("category")

    if selected_category:
        # filter using contains because dataset has hierarchy
        products = products.filter(category__icontains=selected_category)

    # ===============================
    # PRICE FILTER
    # ===============================
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    # ===============================
    # SORTING
    # ===============================
    sort = request.GET.get("sort")

    if sort == "price_low":
        products = products.order_by("price")
    elif sort == "price_high":
        products = products.order_by("-price")
    elif sort == "rating":
        products = products.order_by("-rating")
    else:
        products = products.order_by("-created_at")

    # ===============================
    # CLEAN SIDEBAR CATEGORIES
    # ===============================

    raw_categories = Product.objects.values_list("category", flat=True).distinct()

    cleaned_categories = set()

    for cat in raw_categories:
        if cat:
            # Extract only top-level category
            main_cat = cat.split(">")[0].strip()
            cleaned_categories.add(main_cat)

    categories = sorted(cleaned_categories)

    return render(request, "products/product_list.html", {
        "products": products[:60],
        "categories": categories,
        "selected_category": selected_category,
    })


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    recommendations = recommender_service.get_recommendations(
        product.name,
        top_n=4
    )

    return render(request, "products/product_detail.html", {
        "product": product,
        "recommendations": recommendations
    })