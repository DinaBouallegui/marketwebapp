from django import forms
from .models import User, UserProfile
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

    def clean(self):
        #ovverriding the clean inbuilt function
        cleaned_data = super(UserForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password is not matching")

class UserProfileForm(forms.ModelForm): 
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Start typing...','required' : 'required'}))
    profile_picture = forms.ImageField(widget = forms.FileInput(attrs={'class':'btn btn-info'}))
    cover_photo = forms.ImageField(widget = forms.FileInput(attrs={'class':'btn btn-info'}))
    
    latitude = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    longitude = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta:
        model = UserProfile
        fields = ['profile_picture','cover_photo','address','country',
                  'state','city','pincode','longitude','latitude']
    

# using a diff user form
# creating another user form with only firstname/lastname/number

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','phone_number']