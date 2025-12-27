from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp, name='SignUp'),
    path('login/', views.Login, name='Login'),
    path('logout/', views.Logout, name='Logout'),
    path('edit/<int:srno>', views.Edit, name='Edit'),
    path('delete/<int:srno>', views.Delete, name='Delete'),
]