from django.contrib import admin
from shop.models import *


# Register your models here.
# Registering models in Django Admin panel

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(ShopManager)

