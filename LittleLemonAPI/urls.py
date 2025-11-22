from django.urls import path, include
from . import views

app_name = 'LittleLemonAPI'

urlpatterns = [
    path('menu-items/', views.MenuItems.as_view())
]
