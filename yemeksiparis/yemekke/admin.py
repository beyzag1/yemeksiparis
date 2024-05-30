from django.contrib import admin
from .models import User,ProductCategory,SellerUser,Product,Order,UserProfile

# Register your models here.

admin.site.register(ProductCategory)
admin.site.register(SellerUser)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(UserProfile)
