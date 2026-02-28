from .services.recommender import RecommenderService
recommender_service = RecommenderService()
from django.shortcuts import render


def recommend_view(request):
    recommendations = []

    if request.method == "POST":
        product_name = request.POST.get("product_name")
        top_n = int(request.POST.get("top_n", 5))

        recommendations = recommender_service.get_recommendations(product_name, top_n)

    return render(request, "main.html", {"recommendations": recommendations})

