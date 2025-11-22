from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated

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
            return Response(request.data, status.HTTP_403_FORBIDDEN)

    def put(self, request):
        return Response({'error': 'method not supported'}, status.HTTP_403_FORBIDDEN)
    
    def patch(self, request):
        return Response({'error': 'method not supported'}, status.HTTP_403_FORBIDDEN)
    
    def delete(self, request):
        return Response({'error': 'method not supported'}, status.HTTP_403_FORBIDDEN)