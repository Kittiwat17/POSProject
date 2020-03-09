from django.urls import path
from conclude import views

urlpatterns = [
    path('', views.conclude, name='conclude'),
    
]
