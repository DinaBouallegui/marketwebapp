from django.shortcuts import get_object_or_404, redirect, render
from menu.forms import FoodItemForm
from menu.forms import CategoryForm
from useraccounts.views import check_role_vendor
from useraccounts.forms import UserProfileForm
from .forms import VendorForm 
from menu.models import Category,FoodItem

from django.template.defaultfilters import slugify
from useraccounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test



# Create your views here.

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorProfile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    # by passing these instances inside the form, the form will load the existing content of this particular form
    
    # in case the user updates the form and clicks on submit
    # if request is post means that the user wants to store something inside the database
    if request.method =='POST':
        #  "request.FILES" represents any files uploaded by the user.
        #  "request.POST" represents data uploaded by the user.
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'Settings updated')
            return redirect('vendorProfile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance = profile)
        vendor_form = VendorForm(instance = vendor)

    context ={
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vendorProfile.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    #vendor = Vendor.objects.get(user=request.user)
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor= vendor)
    context = {
        'categories' : categories,
    }
    return render(request,'vendor/menu_builder.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor,category=category)
    context = {
        'fooditems': fooditems,
        'category': category,
    }
    return render(request, 'vendor/fooditems_by_category.html',context)

# a helper function that helps to get the vendor object
def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid(): 
            category_name = form.cleaned_data['category_name']
            #save inside the database
            category = form.save(commit=False)
            #commit = false means this form is ready to be saved but not yet stored
            # assigned the login user to the category vendor field
            category.vendor = get_vendor(request)
            # saligify will generate slug based on categoy_name
            category.slug = slugify(category_name)
            form.save()
            messages.success(request,'Great!Category added successfully!')
            return redirect('menu_builder')
        else: 
            print(form.errors)
    else: 
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category,pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid(): 
            category_name = form.cleaned_data['category_name']
            #save inside the database
            category = form.save(commit=False)
            #commit = false means this form is ready to be saved but not yet stored
            # assigned the login user to the category vendor field
            category.vendor = get_vendor(request)
            # saligify will generate slug based on categoy_name
            category.slug = slugify(category_name)
            form.save()
            messages.success(request,'Category updated successfully!')
            return redirect('menu_builder')
        else: 
            print(form.errors)
    else: 
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'vendor/edit_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request,'Category was deleted successfully!')
    return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid(): 
            foodtitle = form.cleaned_data['food_title']
            #save inside the database
            food = form.save(commit=False)
            #commit = false means this form is ready to be saved but not yet stored
            # assigned the login user to the category vendor field
            food.vendor = get_vendor(request)
            # saligify will generate slug based on categoy_name
            food.slug = slugify(foodtitle)
            form.save()
            messages.success(request,'Great!Food Item added successfully!')
            return redirect('fooditems_by_category',food.category.id)
        else: 
            print(form.errors)
    else: 
        form = FoodItemForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_food.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request, pk=None):
    food = get_object_or_404(FoodItem,pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES,instance=food)
        if form.is_valid(): 
            foodtitle = form.cleaned_data['food_title']
            #save inside the database
            food = form.save(commit=False)
            #commit = false means this form is ready to be saved but not yet stored
            # assigned the login user to the category vendor field
            food.vendor = get_vendor(request)
            # saligify will generate slug based on categoy_name
            food.slug = slugify(foodtitle)
            form.save()
            messages.success(request,'Food Item was updated successfully!')
            return redirect('fooditems_by_category',food.category.id)
        else: 
            print(form.errors)
    else: 
        form = FoodItemForm(instance=food)
    context = {
        'form': form,
        'food': food,
    }
    return render(request, 'vendor/edit_food.html', context)