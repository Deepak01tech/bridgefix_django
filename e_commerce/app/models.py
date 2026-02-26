from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.




class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
        ('manager', 'Manager'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return self.username


# class Product(models.Model):
#     seller = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="products",
#         limit_choices_to={'role': 'seller'}
#     )
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock = models.IntegerField()
#     is_approved = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.name} (Seller: {self.seller.username})"

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'seller'})
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        limit_choices_to={'role': 'customer'}
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product.name} x {self.quantity}"


class Cart(models.Model):
    customer = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart",
        limit_choices_to={'role': 'customer'}
    )

    def __str__(self):
        return f"Cart of {self.customer.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"    
# class user(models.Model):
#     username = models.CharField(max_length=255, unique=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     ismanager = models.BooleanField(default=False)
#     # _default_manager = models.Manager()

#     def __str__(self):
#         return self.username   

# class Seller(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     Products = models.ManyToManyField(Product)

#     # products = models.ManyToManyField(Product, related_name="sellers")
#     quantity = models.IntegerField()
#     is_approved = models.BooleanField(default=False)



    # def __str__(self):
    #     return self.name 


# class create_user(models.Model):
#     username = models.CharField(max_length=255, unique=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)

#     def __str__(self):
#         return self.username


# class Customer(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)

#     def __str__(self):
#         return self.name
    

