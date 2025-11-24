from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    class Meta:
        model = Cart
        fields = ['menuitem', 'quantity', 'price']



class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = serializers.StringRelatedField(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = OrderItem
        fields = ['menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    delivery_crew_id = serializers.IntegerField(write_only=True)
    delivery_crew = serializers.StringRelatedField()
    class Meta:
        model = Order
        fields = ['user', 'orderitem_set', 'delivery_crew', 'delivery_crew_id', 'status', 'total', 'date']
