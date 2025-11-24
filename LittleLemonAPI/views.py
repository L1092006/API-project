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
        return Response({'message: all of your carts have been deleted'}, status=status.HTTP_200_OK)
    




class OrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.groups.filter(name='Manager').exists():
            orders = Order.objects.all()
        elif request.user.groups.filter(name='Delivery crew').exists():
            orders = Order.objects.filter(delivery_crew=request.user)
        else:
            orders = Order.objects.filter(user=request.user)
        serialized = OrderSerializer(orders, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if not (request.user.groups.filter(name='Manager').exists() or request.user.groups.filter(name='Manager').exists()):
            cartItems = Cart.objects.select_related('menuitem').filter(user=request.user)
            
            totalPrice = 0
            for c in cartItems:
                totalPrice += c.price
            
            order = Order(user=request.user, total=totalPrice)
            order.save()

            for c in cartItems:
                orderItem = OrderItem(order=order, menuitem=c.menuitem, quantity=c.quantity, unit_price=c.unit_price, price=c.price)
                orderItem.save()

            cartItems.delete()

            return Response({'message: order created'}, status=status.HTTP_201_CREATED)
        return Response({'error: Unauthorized'})
    
class SingleOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        if not (request.user.groups.filter(name='Manager').exists() or request.user.groups.filter(name='Manager').exists()):
            order = get_object_or_404(Order, id=pk)
            if order.user != request.user:
                return Response({'error': "You don't have this order"}, status=status.HTTP_401_UNAUTHORIZED)

            orderItems = OrderItem.objects.filter(order=order)

            items = [item.menuitem for item in orderItems]
            return Response(MenuItemSerializer(items, many=True).data, status=status.HTTP_200_OK)
        return Response({'error: Unauthorized'})
    
    #Improvement for  put and patch: only allow manager to update the delivery crew and allow customer to update the menuitem
    def put(self, request, pk):
        if not request.user.groups.filter(name='Delivery crew').exists():
            order = get_object_or_404(Order, id=pk)
            if order.user != request.user and not request.user.groups.filter(name='Manager').exists():
                return Response({'error': "You don't have this order"}, status=status.HTTP_401_UNAUTHORIZED)

            serialized = OrderSerializer(order, data=request.data, partial=True)
            serialized.is_valid(raise_exception=True)
            serialized.save()
            
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response({'error: Unauthorized'})

    def patch(self, request, pk):
        if not request.user.groups.filter(name='Delivery crew').exists():
            order = get_object_or_404(Order, id=pk)
            if order.user != request.user and not request.user.groups.filter(name='Manager').exists():
                return Response({'error': "You don't have this order"}, status=status.HTTP_401_UNAUTHORIZED)

            serialized = OrderSerializer(order, data=request.data, partial=True)
            serialized.is_valid(raise_exception=True)
            serialized.save()
            
            return Response(serialized.data, status=status.HTTP_200_OK)
        else:
            order = get_object_or_404(Order, id=pk)
            if order.delivery_crew != request.user:
                return Response({'error': "You don't have this order"}, status=status.HTTP_401_UNAUTHORIZED)

            if not request.data.get('status'):
                return Response({'error': 'Please provide the status'})
            delivered = {'status': request.data.get('status')}
            serialized = OrderSerializer(order, data=delivered, partial=True)
            serialized.is_valid(raise_exception=True)
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)
        
    def delete(self, request, pk):
        if request.user.groups.filter(name='Manager').exists():
            order = get_object_or_404(Order, id=pk)
            order.delete()
            return Response({'message': 'order deleted'}, status=status.HTTP_200_OK)
        return Response({'error': 'unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        
    