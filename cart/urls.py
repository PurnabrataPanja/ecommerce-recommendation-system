from django.urls import path
from .views import add_to_cart, view_cart, remove_from_cart, update_cart_quantity

urlpatterns = [
    path("add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("", view_cart, name="view_cart"),
    path("remove/<int:product_id>/", remove_from_cart, name="remove_from_cart"),
    path("update/<int:product_id>/", update_cart_quantity, name="update_cart_quantity"),
]