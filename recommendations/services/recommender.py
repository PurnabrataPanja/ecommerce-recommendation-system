import os
import pickle
import numpy as np
from products.models import Product
import difflib


class RecommenderService:

    def __init__(self):
        self.vectorizer = None
        self.similarity_matrix = None
        self.product_ids = None
        self._load_model()

    def _load_model(self):
        base_path = "recommendations/ml_models"

        vectorizer_path = os.path.join(base_path, "tfidf_vectorizer.pkl")
        similarity_path = os.path.join(base_path, "similarity_matrix.pkl")

        if not os.path.exists(vectorizer_path) or not os.path.exists(similarity_path):
            raise Exception("Model files not found. Train the model first.")

        with open(vectorizer_path, "rb") as f:
            self.vectorizer = pickle.load(f)

        with open(similarity_path, "rb") as f:
            data = pickle.load(f)
            self.similarity_matrix = data["matrix"]
            self.id_to_index = data["id_to_index"]

    def get_recommendations(self, product_name, top_n=5):

        # 1️ Try partial match first
        product = Product.objects.filter(
            name__icontains=product_name
        ).first()

        # 2️ If not found → use fuzzy match
        if not product:
            all_names = Product.objects.values_list("name", flat=True)

            closest_matches = difflib.get_close_matches(
                product_name,
                all_names,
                n=1,
                cutoff=0.4
            )

            if closest_matches:
                product = Product.objects.filter(
                    name=closest_matches[0]
                ).first()

        if not product:
            return []

        product_id = product.id

        if product_id not in self.id_to_index:
            return []

        index = self.id_to_index[product_id]

        similarity_scores = list(enumerate(self.similarity_matrix[index]))
        similarity_scores = sorted(
            similarity_scores,
            key=lambda x: x[1],
            reverse=True
        )

        recommended_indices = similarity_scores[1: top_n + 1]

        recommended_product_ids = [
            list(self.id_to_index.keys())[i[0]]
            for i in recommended_indices
            ]

        return Product.objects.filter(id__in=recommended_product_ids)