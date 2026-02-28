import csv
from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = "Load products from CSV file"

    def handle(self, *args, **kwargs):
        file_path = "data/products.csv"

        # Optional: Clear existing products before loading
        Product.objects.all().delete()

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                rating = float(row.get("rating", 0) or 0)
                review_count = int(float(row.get("review_count", 0) or 0))

                #  PRICE FIX
                try:
                    price = float(row.get("price", 0) or 0)
                except:
                    price = 0

                Product.objects.create(
                    name=row.get("name"),
                    brand=row.get("brand"),
                    category=row.get("category"),
                    description=row.get("description"),
                    image_url=row.get("image_url"),
                    rating=rating,
                    review_count=review_count,
                    price=price  
                )

        self.stdout.write(self.style.SUCCESS("Products loaded successfully!"))