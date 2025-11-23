from django.urls import path, include
from . import views

app_name = 'LittleLemonAPI'

urlpatterns = [
    path('menu-items/', views.MenuItems.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItem.as_view()),
]
