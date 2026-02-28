from django.shortcuts import render, get_object_or_404
from .models import Product
from recommendations.services.recommender import RecommenderService

recommender_service = RecommenderService()


def product_list_view(request):
    products = Product.objects.all()[:50]  # limit for now
    return render(request, "products/product_list.html", {
        "products": products
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