from django.urls import path, include
from . import views 
from useraccounts import views as AccountViews
#. means the current directory

urlpatterns = [ 
    path('profile/', views.vendorProfile, name ='vendorProfile'),
    path('', AccountViews.vendorDashboard,name='vendor'),
    #path for the menu builder
    path('menu-builder/',views.menu_builder,name='menu_builder'),
    path('menu-builder/category/<int:pk>/',views.fooditems_by_category,name='fooditems_by_category'),
    #this part is for category CRUD
    path('menu-builder/category/add/', views.add_category, name='add_category'),
]