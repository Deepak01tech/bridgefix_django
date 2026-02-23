from django.shortcuts import render, redirect


from django.http import JsonResponse
from .models import Product, Order, Customer, Cart, CartItem, Seller

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User

def home(request):
    # return render(request, 'home.html')
    return JsonResponse({"message": "Welcome to the E-commerce API"})

# @require_POST
def user_login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    if not username or not password:
        return render(request, "login.html", {
            "error": "Username and password are required"
        })

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect("home")   # change 'home' to your home url name
    else:
        return render(request, "login.html", {
            "error": "Invalid username or password"
        })

# def user_login(request):
#     username = request.POST.get("username")
#     password = request.POST.get("password")

#     if not username or not password:
#         return JsonResponse(
#             {"error": "username and password are required"},
#             status=400
#         )

#     user = authenticate(request, username=username, password=password)

#     if user is not None:
#         login(request, user)
#         return JsonResponse({
#             "message": "Login successful",
#             "user_id": user.id,
#             "username": user.username
#         })
#     else:
#         return JsonResponse(
#             {"error": "Invalid username or password"},
#             status=401
#         )

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return render(request, "signup.html", {
                "error": "Username and password are required"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already exists"
            })

        User.objects.create_user(username=username, password=password)
        return redirect("login")  # go to login page after signup

    # GET request → show signup page
    return render(request, "signup.html")

@login_required
@require_POST
def user_logout(request):
    logout(request)
    return JsonResponse({
        "message": "Logged out successfully",
        "status": "success"
    })
@login_required
def product_list(request):
    products = Product.objects.all()
    data = [{"id": p.id, "name": p.name, "description": p.description, "price": str(p.price), "stock": p.stock} for p in products]
    return JsonResponse(data, safe=False)

@login_required
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        data = {"id": product.id, "name": product.name, "description": product.description, "price": str(product.price), "stock": product.stock}
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    
@login_required
def order_list(request):
    orders = Order.objects.all()
    data = [{"id": o.id, "product": o.product.name, "quantity": o.quantity, "total_price": str(o.total_price)} for o in orders]
    return JsonResponse(data, safe=False)

@login_required
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        data = {"id": order.id, "product": order.product.name, "quantity": order.quantity, "total_price": str(order.total_price)}
        return JsonResponse(data)
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found"}, status=404)
    
@login_required
def customer_list(request):
    customers = Customer.objects.all()
    data = [{"id": c.id, "name": c.name, "email": c.email} for c in customers]
    return JsonResponse(data, safe=False)

@login_required
def customer_detail(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
        data = {"id": customer.id, "name": customer.name, "email": customer.email}
        return JsonResponse(data)
    except Customer.DoesNotExist:
        return JsonResponse({"error": "Customer not found"}, status=404)
@login_required   
def cart_detail(request):
    
    cart = Cart.objects.first()
    if cart:
        items = CartItem.objects.filter(cart=cart)
        data = {
            "customer": cart.customer.name,
            "products": [{"name": item.product.name, "quantity": item.quantity} for item in items]
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Cart not found"}, status=404)
    
@login_required   
def add_to_cart(request, product_id):
    # get product using filter
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return JsonResponse({"error": "Product not found"}, status=404)

    # get customer linked to logged-in user
    customer = Customer.objects.filter(user=request.user).first()
    if not customer:
        return JsonResponse({"error": "Customer not found"}, status=404)

    # get or create cart
    cart = Cart.objects.filter(customer=customer).first()
    if not cart:
        cart = Cart.objects.create(customer=customer)

    # check if item already in cart
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1
        )

    return JsonResponse({
        "message": "Product added to cart",
        "product": product.name
    })

@login_required
def remove_from_cart(request, product_id):
    # get product
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return JsonResponse({"error": "Product not found"}, status=404)

    # get customer of logged-in user
    customer = Customer.objects.filter(user=request.user).first()
    if not customer:
        return JsonResponse({"error": "Customer not found"}, status=404)

    # get cart
    cart = Cart.objects.filter(customer=customer).first()
    if not cart:
        return JsonResponse({"error": "Cart not found"}, status=404)

    # get cart item
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if not cart_item:
        return JsonResponse({"error": "Product not in cart"}, status=404)

    # remove item from cart
    cart_item.delete()

    return JsonResponse({
        "message": "Product removed from cart",
        "product": product.name
    })

@login_required
def user_list(request):
    users = User.objects.all()
    data = [{"id": u.id, "username": u.username, "email": u.email} for u in users]
    return JsonResponse(data, safe=False)

@login_required
def user_detail(request, pk):
    try:
        user_obj = User.objects.get(pk=pk)
        data = {"id": user_obj.id, "username": user_obj.username, "email": user_obj.email}
        return JsonResponse(data)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
@login_required  
def seller_list(request):
    sellers = Seller.objects.all()
    data = [{"id": s.id, "name": s.name, "email": s.email} for s in sellers]
    return JsonResponse(data, safe=False)

@login_required
def seller_detail(request, pk):
    try:
        seller = Seller.objects.get(pk=pk)
        data = {"id": seller.id, "name": seller.name, "email": seller.email}
        return JsonResponse(data)
    except Seller.DoesNotExist:
        return JsonResponse({"error": "Seller not found"}, status=404)
    
@login_required  
def seller_products(request, pk):
    try:
        seller = Seller.objects.get(pk=pk)
        products = seller.Products.all()
        data = [{"id": p.id, "name": p.name, "description": p.description, "price": str(p.price), "stock": p.stock} for p in products]
        return JsonResponse(data, safe=False)
    except Seller.DoesNotExist:
        return JsonResponse({"error": "Seller not found"}, status=404)

@login_required
def add_product_to_seller(request, pk):
    # get seller
    seller = Seller.objects.filter(pk=pk).first()
    if not seller:
        return JsonResponse({"error": "Seller not found"}, status=404)

    # get product_id from request
    product_id = request.POST.get("product_id") or request.GET.get("product_id")
    if not product_id:
        return JsonResponse({"error": "product_id is required"}, status=400)

    # get product
    product = Product.objects.filter(pk=product_id).first()
    if not product:
        return JsonResponse({"error": "Product not found"}, status=404)

    # add product to seller
    seller.Products.add(product)   # assuming ManyToManyField
    seller.save()

    return JsonResponse({
        "message": "Product added to seller",
        "seller": seller.name,
        "product": product.name
    })

@login_required
def remove_product_from_seller(request, pk, product_id):
    # get seller
    seller = Seller.objects.filter(pk=pk).first()
    if not seller:
        return JsonResponse({"error": "Seller not found"}, status=404)

    # get product
    product = Product.objects.filter(pk=product_id).first()
    if not product:
        return JsonResponse({"error": "Product not found"}, status=404)

    # check if product belongs to seller
    if not seller.Products.filter(pk=product.pk).exists():
        return JsonResponse({"error": "Product not assigned to this seller"}, status=404)

    # remove product from seller
    seller.Products.remove(product)

    return JsonResponse({
        "message": "Product removed from seller",
        "seller": seller.name,
        "product": product.name
    })

@login_required
def manager_approval(request):
    if request.method == "POST":
        seller_id = request.POST.get("seller_id")

        if not seller_id:
            return render(request, "manager_approval.html", {
                "error": "Seller ID is required"
            })

        seller = Seller.objects.filter(pk=seller_id).first()
        if not seller:
            return render(request, "manager_approval.html", {
                "error": "Seller not found"
            })

        seller.is_approved = True
        seller.save()

        return render(request, "manager_approval.html", {
            "success": f"Seller '{seller.name}' approved successfully"
        })

    
    return render(request, "manager_approval.html")


