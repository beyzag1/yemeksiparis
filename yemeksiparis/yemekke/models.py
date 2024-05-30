
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    telefon = models.CharField(max_length=11)
    adress = models.TextField()

    def __str__(self):
        return self.telefon
    
class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class SellerUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    adress = models.TextField()
    image = models.ImageField(upload_to='restaurants/')
    minimum_order_amount=models.DecimalField(max_digits=10,decimal_places=2,null=True)
    category = models.ManyToManyField(ProductCategory,related_name='categories_in_restaurants')

    def __str__(self):
        return self.name + "'s profiles"
    

class Product(models.Model):
    restoran = models.ForeignKey(SellerUser, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to='product/')

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    restaurant = models.ForeignKey(SellerUser, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)
    order_note = models.TextField(max_length=150, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False)

    def get_total_price(self):
        total = sum(item.product.price * item.quantity for item in self.order_items.all())
        return total

    def clean(self):
        if self.product and self.restaurant != self.product.restaurant:
            raise ValidationError("Selected product must belong to the selected restaurant.")
        super().clean()

    def __str__(self):
        if self.product:
            product_name = self.product.name
        else:
            product_name = "No Product"
        return f"{self.quantity}x {product_name} for {self.user.user.username}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    additional_notes = models.TextField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} for {self.order.user}"

