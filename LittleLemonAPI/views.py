from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from .models import *
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

# Create your views here.
class MenuItemsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        items = MenuItem.objects.all()
        serialized = MenuItemSerializer(items, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if request.user.groups.filter(name='Manager').exists():
            serialized = MenuItemSerializer(data=request.data)
            serialized.is_valid(raise_exception=True)
            serialized.save()
            return Response(serialized.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'unauthorized'}, status.HTTP_403_FORBIDDEN)

    def put(self, request):
        return Response({'error': 'method not supported'}, status.HTTP_403_FORBIDDEN)
    
    def patch(self, request):
        return Response({'error': 'method not supported'}, status.HTTP_403_FORBIDDEN)
    
    def delete(self, request):
        return Response({'error': 'method not supported'}, status.HTTP_403_FORBIDDEN)
    

class SingleMenuItemView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        items = get_object_or_404(MenuItem, id=pk)
        serialized = MenuItemSerializer(items)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        return Response({'error': 'method not supported'}, status.HTTP_403_FORBIDDEN)

    def put_and_patch(self, request, pk):
        if request.user.groups.filter(name='Manager').exists():
            item = get_object_or_404(MenuItem, id=pk)
            serialized = MenuItemSerializer(item, data=request.data, partial=True)
            serialized.is_valid(raise_exception=True)
            serialized.save()
            return Response(serialized.validated_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'unauthorized'}, status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        return self.put_and_patch(request, pk)
    
    def patch(self, request, pk):
        return self.put_and_patch(request, pk)
    
    def delete(self, request, pk):
        if request.user.groups.filter(name='Manager').exists():
            item = get_object_or_404(MenuItem, id=pk)
            item.delete()
            return Response({'message: item deleted'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'unauthorized'}, status.HTTP_403_FORBIDDEN)
        






class ManagersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.groups.filter(name='Manager').exists():
            managers = User.objects.filter(groups__name='Manager')
            serialized = UserSerializer(managers, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response({'error': 'unauthorized'}, status=status.HTTP_403_FORBIDDEN)

    # IMPROVE: SEARCH BY USERNAME INSTEAD OF ID
    def post(self, request):
        if request.user.groups.filter(name='Manager').exists():
            requestId = request.data.get('id')
            if requestId:
                user = get_object_or_404(User, id=requestId)
                group = get_object_or_404(Group, name='Manager')
                user.groups.add(group)
                return Response({'message: user added to Manager group'}, status=status.HTTP_201_CREATED)
            return Response({'error: Please provide an ID'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'unauthorized'}, status.HTTP_403_FORBIDDEN)
        

class SingleManagerView(APIView):
    permission_classes = [IsAuthenticated] 
    def delete(self, request, pk):
        if request.user.groups.filter(name='Manager').exists():
            user = get_object_or_404(User, id=pk)
            group = get_object_or_404(Group, name='Manager')
            user.groups.remove(group)
            return Response({'message: user removed from Manager group'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'unauthorized'}, status.HTTP_403_FORBIDDEN)











class DeliveryCrewsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.groups.filter(name='Manager').exists():
            crews = User.objects.filter(groups__name='Delivery crew')
            serialized = UserSerializer(crews, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response({'error': 'unauthorized'}, status=status.HTTP_403_FORBIDDEN)

    # IMPROVE: SEARCH BY USERNAME INSTEAD OF ID
    def post(self, request):
        if request.user.groups.filter(name='Manager').exists():
            requestId = request.data.get('id')
            if requestId:
                user = get_object_or_404(User, id=requestId)
                group = get_object_or_404(Group, name='Delivery crew')
                user.groups.add(group)
                return Response({'message: user added to Delivery crew group'}, status=status.HTTP_201_CREATED)
            return Response({'error: Please provide an ID'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'unauthorized'}, status.HTTP_403_FORBIDDEN)
        

class SingleDeliveryCrewView(APIView):
    permission_classes = [IsAuthenticated] 
    def delete(self, request, pk):
        if request.user.groups.filter(name='Manager').exists():
            user = get_object_or_404(User, id=pk)
            group = get_object_or_404(Group, name='Delivery crew')
            user.groups.remove(group)
            return Response({'message: user removed from Delivery crew group'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'unauthorized'}, status.HTTP_403_FORBIDDEN)
        


class CartMenuItemsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        items = Cart.objects.filter(user=request.user)
        serialized = CartSerializer(items, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Request data should only have menuitem_title and quantity
        """
        # Init serializer with only quantity, the title is ingored
        serialized = CartSerializer(data=request.data, partial=True)
        serialized.is_valid(raise_exception=True)

        #Get the item by filtering title
        item = get_object_or_404(MenuItem, title=request.data.get('menuitem_title'))

        #Get the item price and calculate unit and final prices
        unit_price = item.price
        price = unit_price * serialized.validated_data.get('quantity')

        #Save the cart item, providing user, menuitem, unit and final prices
        serialized.save(user=request.user, menuitem=item, unit_price=unit_price, price=price)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response({'message: all of your carts deleted'}, status=status.HTTP_200_OK)