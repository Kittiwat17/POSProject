from django.urls import path
from sale import views

urlpatterns = [
    path('login/', views.my_login, name='login'),
    path('signup/', views.my_signup, name='signup'),
    path('', views.index, name='index'),
    
]
