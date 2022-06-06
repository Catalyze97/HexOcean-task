"""
URL mappings for the user API.
"""
from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [

    path('create/', views.CreateUserView.as_view(), name='create'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),

]
