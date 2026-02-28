import os
import pickle
import numpy as np
from django.core.management.base import BaseCommand
from products.models import Product
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Command(BaseCommand):
    help = "Train recommendation model and save it"

    def handle(self, *args, **kwargs):

        products = Product.objects.all()

        if not products.exists():
            self.stdout.write(self.style.ERROR("No products found in database."))
            return

        # Combine text fields
        documents = []
        product_ids = []

        for product in products:
            text = f"{product.name} {product.brand} {product.category} {product.description}"
            documents.append(text)
            product_ids.append(product.id)

        # TF-IDF
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(documents)

        # Cosine Similarity
        similarity_matrix = cosine_similarity(tfidf_matrix)

        # Create ml_models folder
        os.makedirs("recommendations/ml_models", exist_ok=True)

        # Save vectorizer
        with open("recommendations/ml_models/tfidf_vectorizer.pkl", "wb") as f:
            pickle.dump(vectorizer, f)

        # Save similarity matrix
        with open("recommendations/ml_models/similarity_matrix.pkl", "wb") as f:
            pickle.dump({
                "matrix": similarity_matrix,
                "product_ids": product_ids
            }, f)

        self.stdout.write(self.style.SUCCESS("Recommender model trained successfully!"))