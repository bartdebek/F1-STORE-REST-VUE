from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product, Team
from .serializers import ProductSerializer, TeamSerializer


class LatestProductsList(APIView):

    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class TeamsList(APIView):

    def get(self, request, format=None):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

