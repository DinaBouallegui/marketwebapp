from django.urls import path, include
from . import views 
#. means the current directory

urlpatterns = [ 
    path('', views.myAccount),
    path('registerUser/', views.registerUser,name='registerUser'),
    path('registerVendor/', views.registerVendor,name='registerVendor'),
    path('login/', views.login,name='login'),
    path('logout/', views.logout,name='logout'),
    #helps for identification, whether the person is customer or restaurant
    path('myAccount/', views.myAccount ,name='myAccount'),
    path('customerDashboard/', views.customerDashboard,name='customerDashboard'),
    path('vendorDashboard/', views.vendorDashboard,name='vendorDashboard'),
    path('activate/<uidb64>/<token>/', views.activate,name='activate'),
    
    path('vendor/', include('vendor.urls')),
#changes
    path('customer/', include('customers.urls'))

]