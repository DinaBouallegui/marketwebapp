from django import forms
from .models import User
#it comes from django
#we are importing our model user

class UserForm(forms.ModelForm):
    #custom fields
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        #model fields
        # which fields i want to specify in the form
        fields = ['first_name','last_name','username','email','phone_number','password']
