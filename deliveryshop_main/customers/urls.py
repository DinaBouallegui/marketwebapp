from django.urls import path
from useraccounts import views as AccountViews
from . import views


urlpatterns = [
    path('', AccountViews.customerDashboard, name='customer'), 
    path('profile/', views.customerprofile, name='customerprofile'),
    path('my_orders/', views.my_orders, name='customer_my_orders'),
]