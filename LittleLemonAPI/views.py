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
class MenuItems(APIView):
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
    

class SingleMenuItem(APIView):
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
        

class Managers(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.groups.filter(name='Manager').exists():
            managers = User.objects.filter(groups__name='Manager')
            serialized = UserSerializer(managers, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response({'error': 'unauthorized'}, status=status.HTTP_403_FORBIDDEN)

    
    def post(self, request):
        if request.user.groups.filter(name='Manager').exists():
            requestId = request.data.get('id')
            if requestId:
                user = get_object_or_404(User, id=requestId)
                group = get_object_or_404(Group, name='Manager')
                user.groups.add(group)
                return Response({'message: user added to manager group'}, status=status.HTTP_201_CREATED)
            return Response({'error: Please provide an ID'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'unauthorized'}, status.HTTP_403_FORBIDDEN)
