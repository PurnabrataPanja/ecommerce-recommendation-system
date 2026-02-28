from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import CartItem
from products.models import Product


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("view_cart")


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        price = item.product.price or 0
        total += price * item.quantity

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