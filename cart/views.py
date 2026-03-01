from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CartItem
from products.models import Product


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    quantity = 1
    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity", 1))
            if quantity < 1:
                quantity = 1
        except (ValueError, TypeError):
            quantity = 1

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity

    cart_item.save()
    return redirect("view_cart")


@login_required
def update_cart_quantity(request, product_id):
    if request.method == "POST":
        cart_item = get_object_or_404(
            CartItem,
            user=request.user,
            product_id=product_id
        )

        action = request.POST.get("action")

        if action == "increase":
            cart_item.quantity += 1

        elif action == "decrease":
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
                return redirect("view_cart")

        cart_item.save()

    return redirect("view_cart")


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        price = item.product.price or 0
        total += price * item.quantity

    total = round(total, 2)

    return render(request, "cart/cart.html", {
        "cart_items": cart_items,
        "total": total
    })


@login_required
def remove_from_cart(request, product_id):
    CartItem.objects.filter(
        user=request.user,
        product_id=product_id
    ).delete()

    return redirect("view_cart")