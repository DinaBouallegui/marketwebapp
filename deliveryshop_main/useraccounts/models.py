from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models import OneToOneField


#rewriting the django user model so that it fits my model
# Create your models here.
#we inherit the user managers default ones of django and edit the way it works
#this usermanager extends the features of baseusermanager
#it only contains methods and no fields 
class UserManager (BaseUserManager):
    #creating a regular user
    def create_user(self, first_name,last_name,username,email,password=None):
        #basic checks 
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')
        #normalize_email will take your email address upercase and it will be in the form 
        #of lowe case
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        #django uses using parameter to define which databasse you need to use for this operation
        #self._db will take the default database that we have
        user.save(using=self._db)
        return user
     #creating a superuser
    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
        email=self.normalize_email(email),
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


#if you use ABSTRACTUSER django will not give you the full control over its user model
# it will only allow you to add extra fields to your model
#we use ABSTRACTBASEUSER because you want to have full control over djangos user model

class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (VENDOR,'Restaurant'),
        (CUSTOMER,'Customer'),
    )
    #1-adding the fields of the user model
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    phone_number= models.CharField(max_length=12,blank=True)
    #adding roles, role will store 1 or 2
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE,blank=True,null=True)

    #2-fields that are required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True)
    created_date=models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    #by default django uses username as login field but I will override that
    #username itself id a required field
    USERNAME_FIELD='email'

    REQUIRED_FIELDS=['username','first_name','last_name']

    #the user class needs to know which user manager to use in this model
    objects = UserManager()
    
    def __str__(self):
        return self.email
   
    #it will return true if the user is  an admin
    def has_perm(self,perm,obj=None):
        return self.is_admin
    #for inactive users it will return false , by default admin and super admin can only have 
    #access to this model

    #it will return true if the user is  a active superuser
    def has_module_perms(self,app_label):
        return True
    #can be accessed as it's field
    def get_role(self):
        user_role = ""
        if self.role == 1:
            user_role = 'Vendor'
        elif self.role == 2:
            user_role ='Customer'
        return user_role

class UserProfile(models.Model):
    user = OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    #if the user is deleted his user profile also should be deleted
    #profile_picture and cover_photo
    #The upload_to argument specifies the directory path within the MEDIA_ROOT directory where the uploaded image file will be stored. 
    #blank=True means that the field is allowed to be blank, the user is allowed to not write values
    #null=True means that the field is allowed to be NULL in the database
    profile_picture = models.ImageField(upload_to='users/profile_pictures',blank=True,null=True)
    #must install pillow library whenevr imagefield is used
    cover_photo = models.ImageField(upload_to='users/cover_photo',blank=True,null=True)
    address_line_1=models.CharField(max_length=50,blank=True,null=True)
    address_line_2=models.CharField(max_length=50,blank=True,null=True)
    country=models.CharField(max_length=15,blank=True,null=True)
    state=models.CharField(max_length=15,blank=True,null=True)
    city=models.CharField(max_length=15,blank=True,null=True)
    pincode=models.CharField(max_length=6,blank=True,null=True)
    longitude=models.CharField(max_length=20,blank=True,null=True)
    latitude=models.CharField(max_length=20,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    #auto_now_add=True is set, Django will automatically set the value of the field to the current date 
    # and time when a new instance of the model is created
    modified_at=models.DateTimeField(auto_now=True)
    #__str__() is defined to return the email address of the user associated with that profile
    def __str__(self):
        return self.user.email

