from django.shortcuts import render, redirect


# from django.http import JsonResponse
from .models import Product, Order, Cart, CartItem, User

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
# from django.contrib.auth.models import User

def home(request):
    products = Product.objects.filter(is_approved=False)
    # products = Product.objects.filter(is_approved=True)

    return render(request, 'home.html',{ "products": products})
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
        return redirect("home")   
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
        email = request.POST.get("email")
        role = request.POST.get("role")  

        if not username or not password:
            return render(request, "signup.html", {
                "error": "Username and password are required"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already exists"
            })

        # create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # assign role to THAT user
        user.role = role
        user.save()

        return redirect("login")

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
    # customers = Customer.objects.all()
    customers= User.objects.filter(role='customer')
    # data = [{"id": c.id, "name": c.name, "email": c.email} for c in customers]
    data=[{"id": c.id, "username": c.username, "email": c.email} for c in customers]
    # return JsonResponse(data, safe=False)
    return render(request, "customer_list.html", {"customers": customers})

@login_required
def customer_detail(request, pk):
    try:
        # customer = Customer.objects.get(pk=pk)
        customer = User.objects.filter(pk=pk, role='customer').first()
        # data = {"id": customer.id, "name": customer.name, "email": customer.email}
        data = {"id": customer.id, "username": customer.username, "email": customer.email}
        # return JsonResponse(data)
        return render(request, "customer_detail.html", {"customer": customer})
    # except Customer.DoesNotExist:
    except User.DoesNotExist:
        # return JsonResponse({"error": "Customer not found"}, status=404)
        return render(request, "customer_detail.html", {"error": "Customer not found"})
@login_required 
def cart_detail(request):
    # get cart of logged-in customer
    cart = Cart.objects.filter(customer=request.user).first()

    if cart:
        cart_items = cart.items.all()  # related_name="items"
    else:
        cart_items = []

    grand_total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, "cart_detail.html", {
        "cart_items": cart_items,
        "grand_total": grand_total,
    })
# def cart_detail(request):
    
#     cart = Cart.objects.first()
#     if cart:
#         items = CartItem.objects.filter(cart=cart)
#         data = {
#             # "customer": cart.customer.name,
#             "customer": cart.customer.username,
#             "products": [{"name": item.product.name, "quantity": item.quantity} for item in items]
#         }
#         # return JsonResponse(data)
#         return render(request, "cart_detail.html", {"cart": cart, "items": items})
#     else:
#         # return JsonResponse({"error": "Cart not found"}, status=404)
#         return render(request, "cart_detail.html", {"error": "Cart not found"})
    
@login_required   
def add_to_cart(request, product_id):
    # get product using filter
    product = Product.objects.filter(id=product_id).first()
    if not product:
        # return JsonResponse({"error": "Product not found"}, status=404)
        return render(request, "add_to_cart.html", {"error": "Product not found"})

    # get customer linked to logged-in user
    # customer = Customer.objects.filter(user=request.user).first()
    customer = User.objects.filter(id=request.user.id, role='customer').first()
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
    # customer = Customer.objects.filter(user=request.user).first()
    customer = User.objects.filter(id=request.user.id, role='customer').first()
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
def checkout(request):
    cart = Cart.objects.filter(customer=request.user).first()

    if not cart:
        return render(request, "checkout.html", {"cart_items": [], "grand_total": 0})

    cart_items = cart.items.all()
    # grand_total = sum(item.total_price for item in cart_items)
    grand_total=sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":
       
        cart.items.all().delete()  
        return render(request, "checkout.html", {
            "message": "Order placed successfully 🎉",
            "cart_items": [],
            "grand_total": 0
        })

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "grand_total": grand_total
    })




# @login_required
# def user_list(request):
#     users = User.objects.all()
#     data = [{"id": u.id, "username": u.username, "email": u.email} for u in users]
#     # return JsonResponse(data, safe=False)
#     return render(request, "user_list.html", {"users": users})

@login_required
def user_detail(request, pk):
    try:
        user_obj = User.objects.get(pk=pk)
        # data = {"id": user_obj.id, "username": user_obj.username, "email": user_obj.email}
        # return JsonResponse(data)
        return render(request, "user_detail.html", {"user": user_obj})
    except User.DoesNotExist:
        # return JsonResponse({"error": "User not found"}, status=404)
        return render(request, "user_detail.html", {"error": "User not found"})
# @login_required  
# def seller_list(request):
#     # sellers = Seller.objects.all()
#     sellers = User.objects.filter(role='seller')
#     # data = [{"id": s.id, "name": s.name, "email": s.email} for s in sellers]
#     data = [{"id": s.id, "username": s.username, "email": s.email} for s in sellers]
#     # return JsonResponse(data, safe=False)
#     return render(request, "seller_list.html", {"sellers": sellers})

@login_required
def seller_detail(request, pk):
    try:
        # seller = Seller.objects.get(pk=pk)
        seller = User.objects.filter(pk=pk, role='seller').first()
        # data = {"id": seller.id, "name": seller.name, "email": seller.email}
        data = {"id": seller.id, "username": seller.username, "email": seller.email}
        # return JsonResponse(data)
        return render(request, "seller_detail.html", {"seller": seller})
    # except Seller.DoesNotExist:
    except User.DoesNotExist:
        # return JsonResponse({"error": "Seller not found"}, status=404)
        return render(request, "seller_detail.html", {"error": "Seller not found"})
    
@login_required
def seller_products(request):
    if request.user.role != "seller":
        return render(request, "error.html", {"error": "Only sellers allowed"})

    products = Product.objects.filter(seller=request.user)
    return render(request, "seller_products.html", {"products": products})
    
# @login_required  
# def seller_products(request, pk):
#     try:
#         # seller = Seller.objects.get(pk=pk)
#         seller = User.objects.filter(pk=pk, role='seller').first()
#         # products = seller.Products.all()
#         products = Product.objects.filter(seller=seller)
#         data = [{"id": p.id, "name": p.name, "description": p.description, "price": str(p.price), "stock": p.stock} for p in products]
#         # return JsonResponse(data, safe=False)
#         return render(request, "seller_products.html", {"seller": seller, "products": products})
#     # except Seller.DoesNotExist:
#     except User.DoesNotExist:
#         # return JsonResponse({"error": "Seller not found"}, status=404)
#         return render(request, "seller_products.html", {"error": "Seller not found"})


# @login_required
# def add_product_to_seller(request, pk):             
#     seller = User.objects.filter(pk=pk, role='seller').first()
#     if not seller:
#         return render(request, "add_product_to_seller.html", {"error": "Seller not found"})
#     if seller != request.user:
#         return render(request, "add_product_to_seller.html", {"error": "Not allowed"})

#     products = Product.objects.all()

#     if request.method == "POST":
#         product_id = request.POST.get("product_id")

#         if not product_id:
#             return render(request, "add_product_to_seller.html", {
#                 "error": "Product is required",
#                 "products": products
#             })

#         product = Product.objects.filter(pk=product_id).first()
#         if not product:
#             return render(request, "add_product_to_seller.html", {
#                 "error": "Product not found",
#                 "products": products
#             })

       
#         product.seller = seller
#         product.is_approved = False   
#         product.save()

#         return render(request, "add_product_to_seller.html", {
#             "message": f"Product '{product.name}' added to seller '{seller.username}'",
#             "products": products
#         })

#     return render(request, "add_product_to_seller.html", {"products": products})


@login_required
def add_product(request):
    if request.user.role != "seller":
        return render(request, "add_product_to_seller.html", {"error": "Only sellers can add products"})

    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        stock = request.POST.get("stock") 
        description = request.POST.get("description")
        image = request.FILES.get("image")

        print("DEBUG:", name, price, stock)

        if not name or not price or not stock:
            return render(request, "add_product_to_seller.html", {
                "error": "Product name , price and stock are required"
            })

        Product.objects.create(
            name=name,
            price=price,
            stock=stock,
            description=description,
            image=image,
            seller=request.user,
            is_approved=False
        )
        print("POST:", request.POST)
        print("FILES:", request.FILES)
        return render(request, "add_product_to_seller.html", {
            "success": "Product added successfully"
        })

    return render(request, "add_product_to_seller.html")

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

# @login_required
# def remove_product_from_seller(request, pk, product_id):
#     # get seller
#     # seller = Seller.objects.filter(pk=pk).first()
#     seller = User.objects.filter(pk=pk, role='seller').first()
#     if not seller:
#         # return JsonResponse({"error": "Seller not found"}, status=404)
#         return render(request, "remove_product_from_seller.html", {"error": "Seller not found"})

#     # get product
#     product = Product.objects.filter(pk=product_id).first()
#     if not product:
#         # return JsonResponse({"error": "Product not found"}, status=404)
#         return render(request, "remove_product_from_seller.html", {"error": "Product not found"})

#     # check if product belongs to seller
#     # if not seller.Products.filter(pk=product.pk).exists():
#     if not Product.objects.filter(pk=product.pk, seller=seller).exists():
#         # return JsonResponse({"error": "Product not assigned to this seller"}, status=404)
#         return render(request, "remove_product_from_seller.html", {"error": "Product not assigned to this seller"})

#     # remove product from seller
#     # seller.Products.remove(product)
#     product.seller = None
#     product.save()

#     # return JsonResponse({
#     #     "message": "Product removed from seller",
#     #     "seller": seller.name,
#     #     "product": product.name
#     # })
#     return render(request, "remove_product_from_seller.html", {"message": f"Product '{product.name}' removed from seller '{seller.username}'"})

@login_required
def edit_product(request, pk):
    product = Product.objects.filter(pk=pk, seller=request.user).first()

    if not product:
        return render(request, "edit_product.html", {"error": "Product not found"})

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")
        product.description = request.POST.get("description")

        if request.FILES.get("image"):
            product.image = request.FILES.get("image")

        product.save()
        return render(request, "edit_product.html", {"success": "Product updated successfully", "product": product})

    return render(request, "edit_product.html", {"product": product})

@login_required
def remove_product_from_seller(request, product_id):
    seller = request.user

    
    if seller.role != "seller":
        return render(request, "remove_product_from_seller.html", {
            "error": "Only sellers can remove products"
        })

    
    product = Product.objects.filter(id=product_id, seller=seller).first()

    if not product:
        return render(request, "remove_product_from_seller.html", {
            "error": "Product not found or not yours"
        })

    
    product.delete()
    

    return render(request, "remove_product_from_seller.html", {
        "message": f"Product '{product.name}' removed successfully"
    })

@login_required
def manager_approval(request):
    
    if request.user.role != "manager":
        return render(request, "manager_approval.html", {
            "error": "Only manager can approve products"
        })

    
    products = Product.objects.filter(is_approved=False)

    if request.method == "POST":
        product_id = request.POST.get("product_id")

        if not product_id:
            return render(request, "manager_approval.html", {
                "error": "Product ID is required",
                "products": products
            })

        product = Product.objects.filter(pk=product_id).first()
        if not product:
            return render(request, "manager_approval.html", {
                "error": "Product not found",
                "products": products
            })

        product.is_approved = True
        product.save()

        return render(request, "manager_approval.html", {
            "success": f"Product '{product.name}' approved successfully",
            "products": Product.objects.filter(is_approved=False)
        })

    return render(request, "manager_approval.html", {
        "products": products
    })

# @login_required
# def manager_approval(request):
#     if request.method == "POST":
#         seller_id = request.POST.get("seller_id")

#         if not seller_id:
#             return render(request, "manager_approval.html", {
#                 "error": "Seller ID is required"
#             })

#         # seller = Seller.objects.filter(pk=seller_id).first()
#         seller = User.objects.filter(pk=seller_id, role='seller').first()
#         if not seller:
#             return render(request, "manager_approval.html", {
#                 "error": "Seller not found"
#             })

#         # seller.is_approved = True

#         seller.save()

#         return render(request, "manager_approval.html", {
#             "success": f"Seller '{seller.name}' approved successfully"
#         })

    
#     return render(request, "manager_approval.html")


