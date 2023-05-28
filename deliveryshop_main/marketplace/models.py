from django.db import models
from useraccounts.models import User
from menu.models import FoodItem

class Cart(models.Model):
    # you have to be logged in in order to add the product to the cart
    user = models.ForeignKey(User,on_delete= models.CASCADE)
    fooditem = models.ForeignKey(FoodItem,on_delete= models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicoode__(self):
        return self.user
    
