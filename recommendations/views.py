from .services.recommender import RecommenderService
recommender_service = RecommenderService()
from django.shortcuts import render
from django.http import JsonResponse


def recommend_view(request):
    recommendations = []

    if request.method == "POST":
        product_name = request.POST.get("product_name")
        top_n = int(request.POST.get("top_n", 5))

        recommendations = recommender_service.get_recommendations(product_name, top_n)

    return render(request, "main.html", {"recommendations": recommendations})

def recommend_api(request):

    product_name = request.GET.get("product")
    top_n = int(request.GET.get("top_n", 5))

    if not product_name:
        return JsonResponse({"error": "Product name required"}, status=400)

    recommendations = recommender_service.get_recommendations(product_name, top_n)

    data = []

    for product in recommendations:
        data.append({
            "id": product.id,
            "name": product.name,
            "brand": product.brand,
            "category": product.category,
            "rating": product.rating,
            "image_url": product.image_url
        })

    return JsonResponse({
        "query": product_name,
        "count": len(data),
        "results": data
    })