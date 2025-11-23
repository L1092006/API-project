from django.urls import path, include
from . import views

app_name = 'LittleLemonAPI'

urlpatterns = [
    path('menu-items/', views.MenuItems.as_view()),
    path('menu-items/<int:pk>/', views.SingleMenuItem.as_view()),
    path('groups/manager/users/', views.Managers.as_view()),
    # path('groups/manager/users/<int:pk>/', views.SingleManager.as_view()),
    # path('groups/delivery-crew/users/', views.DeliveryCrews.as_view()),
    # path('groups/delivery-crew/users/<int:pk>/', views.SingleDeliveryCrew.as_view()),
]
