from django.db import models

# Create your models here.

class create_user(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order of {self.quantity} {self.product.name}(s) - Total: ${self.total_price}"

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart of {self.customer.name}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.customer.name}'s cart"
    
class user(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    ismanager = models.BooleanField(default=False)
    # _default_manager = models.Manager()

    def __str__(self):
        return self.username   

class Seller(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    Products = models.ManyToManyField(Product)

    # products = models.ManyToManyField(Product, related_name="sellers")
    quantity = models.IntegerField()
    is_approved = models.BooleanField(default=False)



    def __str__(self):
        return self.name 
    

