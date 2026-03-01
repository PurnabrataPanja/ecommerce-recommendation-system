from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.checkout_review, name="checkout_review"),
    path("confirm/", views.confirm_order, name="confirm_order"),
    path("success/<int:order_id>/", views.order_success, name="order_success"),
    path("history/", views.order_history, name="order_history"),
]