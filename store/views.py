from django.views.decorators.cache import cache_page
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem, Order

@cache_page(60 * 5)  # کش به مدت ۵ دقیقه
def product_list(request):
    products = Product.objects.filter(available=True)
    return render(request, "store/product_list.html", {"products": products})

def cart_detail(request):
    cart = request.session.get("cart", {})
    cart_items = []
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        cart_items.append({"product": product, "quantity": quantity})
    return render(request, "store/cart_detail.html", {"cart_items": cart_items})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    cart = request.session.get("cart", {})
    if str(product.id) in cart:
        cart[str(product.id)] += quantity
    else:
        cart[str(product.id)] = quantity
    request.session["cart"] = cart
    return redirect("store:cart_detail")

def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
        request.session["cart"] = cart
    return redirect("store:cart_detail")

def update_cart(request, product_id):
    cart = request.session.get("cart", {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            cart[product_id_str] = quantity
        else:
            del cart[product_id_str]
        request.session["cart"] = cart
    return redirect("store:cart_detail")
def checkout(request):
    cart = request.session.get("cart", {})
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        
        if cart:  # اگر سبد خالی نباشد
            order = Order.objects.create(
                full_name=full_name,
                email=email,
                address=address,
                paid=False  # چون فعلاً پرداخت نداریم
            )
            # بعد از ثبت سفارش، سبد خالی می‌شود
            request.session["cart"] = {}
            return render(request, "store/checkout_success.html", {"order": order})
    
    # محاسبه محصولات برای نمایش
    cart_items = []
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        cart_items.append({"product": product, "quantity": quantity})
    
    return render(request, "store/checkout.html", {"cart_items": cart_items})