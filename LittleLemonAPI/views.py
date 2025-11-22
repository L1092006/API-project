from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from .models import *

# Create your views here.
def menuItems(APIview):
    def get(self):
        items = MenuItem.objects.all()
        serialized = MenuSerializer(items, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)