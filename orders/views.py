from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from decimal import Decimal
from cart.models import CartItem
from .models import Order, OrderItem
from django.http import HttpResponseBadRequest


@login_required
def checkout_review(request):

    cart_items = CartItem.objects.select_related("product").filter(user=request.user)

    if not cart_items.exists():
        return redirect("view_cart")

    total = Decimal("0.00")

    enriched_items = []

    for item in cart_items:
        subtotal = item.product.price * item.quantity
        total += subtotal

        enriched_items.append({
            "product": item.product,
            "quantity": item.quantity,
            "price": item.product.price,
            "subtotal": subtotal
        })

    return render(request, "orders/checkout_review.html", {
        "cart_items": enriched_items,
        "total": total
    })
@login_required
@transaction.atomic
def confirm_order(request):

    if request.method != "POST":
        return redirect("checkout_review")

    cart_items = CartItem.objects.select_related("product").filter(user=request.user)

    if not cart_items.exists():
        return redirect("view_cart")

    total = Decimal("0.00")

    for item in cart_items:
        total += item.product.price * item.quantity

    order = Order.objects.create(
    user=request.user,
    total_amount=total,
    status="PENDING"
)
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart_items.delete()

    return redirect("payment_page", order_id=order.id)


@login_required
@login_required
def order_success(request, order_id):

    order = Order.objects.get(id=order_id, user=request.user)

    if order.status == "PENDING":
        return redirect("payment_page", order_id=order.id)

    if order.status == "CANCELLED":
        return redirect("order_failed", order_id=order.id)

    return render(request, "orders/order_success.html", {
        "order": order
    })

@login_required
def order_history(request):

    orders = request.user.orders.all().order_by("-created_at")

    return render(request, "orders/order_history.html", {
        "orders": orders
    })





@login_required
def payment_page(request, order_id):

    order = Order.objects.get(id=order_id, user=request.user)

    if order.status != "PENDING":
        return redirect("order_success", order_id=order.id)

    return render(request, "orders/payment_page.html", {
        "order": order
    })


@login_required
@transaction.atomic
def process_payment(request, order_id):

    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request")

    order = Order.objects.select_for_update().get(
        id=order_id,
        user=request.user
    )

    if order.status != "PENDING":
        return redirect("order_success", order_id=order.id)

    # 🔥 Fake payment success simulation
    payment_result = request.POST.get("payment_result")

    if payment_result == "success":
        order.status = "COMPLETED"
        order.save()
        return redirect("order_success", order_id=order.id)

    else:
        order.status = "CANCELLED"
        order.save()
        return redirect("order_failed", order_id=order.id)


@login_required
def order_failed(request, order_id):

    order = Order.objects.get(id=order_id, user=request.user)

    return render(request, "orders/order_failed.html", {
        "order": order
    })