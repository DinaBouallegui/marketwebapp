from django.urls import path, include
from . import views 
from useraccounts import views as AccountViews
#. means the current directory

urlpatterns = [ 
    path('profile/', views.vendorProfile, name ='vendorProfile'),
    path('', AccountViews.vendorDashboard,name='vendor'),
]