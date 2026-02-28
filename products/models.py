from django.db import models


class Product(models.Model):

    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True, null=True)

    
    category = models.CharField(max_length=255, blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    rating = models.FloatField(default=0.0)
    review_count = models.IntegerField(default=0)

    price = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name