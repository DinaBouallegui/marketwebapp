from django import forms

from .models import Category, FoodItem

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        # only category name and description should be entered by the user
        fields =['category_name','description']
        # other things are handled programatically

class FoodItemForm(forms.ModelForm):
    class Meta:

        model = FoodItem
        #these will be by the user
        fields =['category','food_title','description','price','image','is_available']