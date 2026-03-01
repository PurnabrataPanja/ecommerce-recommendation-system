from django.db import models
from decimal import Decimal


class Product(models.Model):

    name = models.CharField(max_length=255, db_index=True)
    brand = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    category = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    rating = models.FloatField(default=0.0, db_index=True)
    review_count = models.IntegerField(default=0)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        db_index=True
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["price"]),
            models.Index(fields=["rating"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["category"]),
            models.Index(fields=["brand"]),
        ]

    def __str__(self):
        return self.name