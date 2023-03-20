from django.urls import path
from . import views #. means the current directory

urlpatterns = [ 
    path('registerUser/', views.registerUser,name='registerUser')
]