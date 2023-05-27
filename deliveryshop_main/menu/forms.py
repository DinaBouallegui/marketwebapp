from django import forms

from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        # only category name and description should be entered by the user
        fields =['category_name','description']
        # other things are handled programatically