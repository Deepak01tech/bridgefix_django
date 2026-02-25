from django.shortcuts import render, redirect


from django.http import JsonResponse
from .models import Product, Order, Customer, Cart, CartItem, Seller

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home.html')
    # return JsonResponse({"message": "Welcome to the E-commerce API"})

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
        return redirect("user_login")  

   
    return render(request, "signup.html")

@login_required
# @require_POST
def user_logout(request):
    logout(request)
    # return JsonResponse({
    #     "message": "Logged out successfully",
    #     "status": "success"
    # })
    return redirect("home")  
@login_required
def product_list(request):
    products = Product.objects.all()
    data = [{"id": p.id, "name": p.name, "description": p.description, "price": str(p.price), "stock": p.stock} for p in products]
    # return JsonResponse(data, safe=False)
    return render(request, "product_list.html", {"products": products})

@login_required
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        data = {"id": product.id, "name": product.name, "description": product.description, "price": str(product.price), "stock": product.stock}
        # return JsonResponse(data)
        return render(request, "product_detail.html", {"product": product})
    except Product.DoesNotExist:
        # return JsonResponse({"error": "Product not found"}, status=404)
        return render(request, "product_detail.html", {"error": "Product not found"})
    
@login_required
def order_list(request):
    orders = Order.objects.all()
    data = [{"id": o.id, "product": o.product.name, "quantity": o.quantity, "total_price": str(o.total_price)} for o in orders]
    # return JsonResponse(data, safe=False)
    return render(request, "order_list.html", {"orders": orders})

@login_required
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        data = {"id": order.id, "product": order.product.name, "quantity": order.quantity, "total_price": str(order.total_price)}
        # return JsonResponse(data)
        return render(request, "order_detail.html", {"order": order})
    except Order.DoesNotExist:
        # return JsonResponse({"error": "Order not found"}, status=404)
        return render(request, "order_detail.html", {"error": "Order not found"})
    
@login_required
def customer_list(request):
    customers = Customer.objects.all()
    data = [{"id": c.id, "name": c.name, "email": c.email} for c in customers]
    # return JsonResponse(data, safe=False)
    return render(request, "customer_list.html", {"customers": customers})

@login_required
def customer_detail(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
        data = {"id": customer.id, "name": customer.name, "email": customer.email}
        # return JsonResponse(data)
        return render(request, "customer_detail.html", {"customer": customer})
    except Customer.DoesNotExist:
        # return JsonResponse({"error": "Customer not found"}, status=404)
        return render(request, "customer_detail.html", {"error": "Customer not found"})
@login_required   
def cart_detail(request):
    
    cart = Cart.objects.first()
    if cart:
        items = CartItem.objects.filter(cart=cart)
        data = {
            "customer": cart.customer.name,
            "products": [{"name": item.product.name, "quantity": item.quantity} for item in items]
        }
        # return JsonResponse(data)
        return render(request, "cart_detail.html", {"cart": cart, "items": items})
    else:
        # return JsonResponse({"error": "Cart not found"}, status=404)
        return render(request, "cart_detail.html", {"error": "Cart not found"})
    
@login_required   
def add_to_cart(request, product_id):
    # get product using filter
    product = Product.objects.filter(id=product_id).first()
    if not product:
        # return JsonResponse({"error": "Product not found"}, status=404)
        return render(request, "add_to_cart.html", {"error": "Product not found"})

    # get customer linked to logged-in user
    customer = Customer.objects.filter(user=request.user).first()
    if not customer:
        # return JsonResponse({"error": "Customer not found"}, status=404)
        return render(request, "add_to_cart.html", {"error": "Customer not found"})

  
    cart = Cart.objects.filter(customer=customer).first()
    if not cart:
        cart = Cart.objects.create(customer=customer)

  
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

    # return JsonResponse({
    #     "message": "Product added to cart",
    #     "product": product.name
    # })
    return render(request, "add_to_cart.html", {"message": f"Product '{product.name}' added to cart"})

@login_required
def remove_from_cart(request, product_id):
    # get product
    product = Product.objects.filter(id=product_id).first()
    if not product:
        # return JsonResponse({"error": "Product not found"}, status=404)
        return render(request, "remove_from_cart.html", {"error": "Product not found"})

    # get customer of logged-in user
    customer = Customer.objects.filter(user=request.user).first()
    if not customer:
        # return JsonResponse({"error": "Customer not found"}, status=404)
        return render(request, "remove_from_cart.html", {"error": "Customer not found"})

    # get cart
    cart = Cart.objects.filter(customer=customer).first()
    if not cart:
        # return JsonResponse({"error": "Cart not found"}, status=404)
        return render(request, "remove_from_cart.html", {"error": "Cart not found"})

    # get cart item
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if not cart_item:
        # return JsonResponse({"error": "Product not in cart"}, status=404)
        return render(request, "remove_from_cart.html", {"error": "Product not in cart"})

    # remove item from cart
    cart_item.delete()

    # return JsonResponse({
    #     "message": "Product removed from cart",
    #     "product": product.name
    # })
    return render(request, "remove_from_cart.html", {"message": f"Product '{product.name}' removed from cart"})

@login_required
def user_list(request):
    users = User.objects.all()
    data = [{"id": u.id, "username": u.username, "email": u.email} for u in users]
    # return JsonResponse(data, safe=False)
    return render(request, "user_list.html", {"users": users})

@login_required
def user_detail(request, pk):
    try:
        user_obj = User.objects.get(pk=pk)
        data = {"id": user_obj.id, "username": user_obj.username, "email": user_obj.email}
        # return JsonResponse(data)
        return render(request, "user_detail.html", {"user": user_obj})
    except User.DoesNotExist:
        # return JsonResponse({"error": "User not found"}, status=404)
        return render(request, "user_detail.html", {"error": "User not found"})
@login_required  
def seller_list(request):
    sellers = Seller.objects.all()
    data = [{"id": s.id, "name": s.name, "email": s.email} for s in sellers]
    # return JsonResponse(data, safe=False)
    return render(request, "seller_list.html", {"sellers": sellers})

@login_required
def seller_detail(request, pk):
    try:
        seller = Seller.objects.get(pk=pk)
        data = {"id": seller.id, "name": seller.name, "email": seller.email}
        # return JsonResponse(data)
        return render(request, "seller_detail.html", {"seller": seller})
    except Seller.DoesNotExist:
        # return JsonResponse({"error": "Seller not found"}, status=404)
        return render(request, "seller_detail.html", {"error": "Seller not found"})
    
@login_required  
def seller_products(request, pk):
    try:
        seller = Seller.objects.get(pk=pk)
        products = seller.Products.all()
        data = [{"id": p.id, "name": p.name, "description": p.description, "price": str(p.price), "stock": p.stock} for p in products]
        # return JsonResponse(data, safe=False)
        return render(request, "seller_products.html", {"seller": seller, "products": products})
    except Seller.DoesNotExist:
        # return JsonResponse({"error": "Seller not found"}, status=404)
        return render(request, "seller_products.html", {"error": "Seller not found"})


@login_required
def add_product_to_seller(request, pk):             
    seller = Seller.objects.filter(pk=pk).first()
    if not seller:
        return render(request, "add_product_to_seller.html", {"error": "Seller not found"})

    # OPTIONAL: ensure only seller owner can add products
    if seller.user != request.user:
        return render(request, "add_product_to_seller.html", {"error": "Not allowed"})

    products = Product.objects.all()

    if request.method == "POST":
        product_id = request.POST.get("product_id")

        if not product_id:
            return render(request, "add_product_to_seller.html", {
                "error": "Product is required",
                "products": products
            })

        product = Product.objects.filter(pk=product_id).first()
        if not product:
            return render(request, "add_product_to_seller.html", {
                "error": "Product not found",
                "products": products
            })

        seller.Products.add(product)

        return render(request, "add_product_to_seller.html", {
            "message": f"Product '{product.name}' added to seller '{seller.name}'",
            "products": products
        })

    return render(request, "add_product_to_seller.html", {"products": products})


# @login_required
# def add_product_to_seller(request, pk):
#     # get seller
#     seller = Seller.objects.filter(pk=pk).first()
#     if not seller:
#         # return JsonResponse({"error": "Seller not found"}, status=404)
#         return render(request, "add_product_to_seller.html", {"error": "Seller not found"})

#     # get product_id from request
#     product_id = request.POST.get("product_id") or request.GET.get("product_id")
#     if not product_id:
#         # return JsonResponse({"error": "product_id is required"}, status=400)
#         return render(request, "add_product_to_seller.html", {"error": "product_id is required"})

#     # get product
#     product = Product.objects.filter(pk=product_id).first()
#     if not product:
#         # return JsonResponse({"error": "Product not found"}, status=404)
#         return render(request, "add_product_to_seller.html", {"error": "Product not found"})

#     # add product to seller
#     seller.Products.add(product)   # assuming ManyToManyField
#     seller.save()

#     # return JsonResponse({
#     #     "message": "Product added to seller",
#     #     "seller": seller.name,
#     #     "product": product.name
#     # })
#     return render(request, "add_product_to_seller.html", {"message": f"Product '{product.name}' added to seller '{seller.name}'"})

@login_required
def remove_product_from_seller(request, pk, product_id):
    # get seller
    seller = Seller.objects.filter(pk=pk).first()
    if not seller:
        # return JsonResponse({"error": "Seller not found"}, status=404)
        return render(request, "remove_product_from_seller.html", {"error": "Seller not found"})

    # get product
    product = Product.objects.filter(pk=product_id).first()
    if not product:
        # return JsonResponse({"error": "Product not found"}, status=404)
        return render(request, "remove_product_from_seller.html", {"error": "Product not found"})

    # check if product belongs to seller
    if not seller.Products.filter(pk=product.pk).exists():
        # return JsonResponse({"error": "Product not assigned to this seller"}, status=404)
        return render(request, "remove_product_from_seller.html", {"error": "Product not assigned to this seller"})

    # remove product from seller
    seller.Products.remove(product)

    # return JsonResponse({
    #     "message": "Product removed from seller",
    #     "seller": seller.name,
    #     "product": product.name
    # })
    return render(request, "remove_product_from_seller.html", {"message": f"Product '{product.name}' removed from seller '{seller.name}'"})

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


