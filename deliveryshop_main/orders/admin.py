from django.contrib import admin
from .models import OrderedFood,Payment,Order
# Register your models here.

admin.site.register(Order)
admin.site.register(OrderedFood)
admin.site.register(Payment)

