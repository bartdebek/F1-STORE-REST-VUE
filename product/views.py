from django.http import Http404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Category, Product, Team
from .serializers import ProductSerializer, TeamSerializer, CategorySerializer


class LatestProductsListView(APIView):

    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class TeamsListView(APIView):

    def get(self, request, format=None):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)


class TeamsProductsView(APIView):

    def get(self, request, team_slug, format=None):
        products = Product.objects.filter(team__slug=team_slug)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
        

# class TeamProductDetailView(APIView):

#     def get_object(self, team_slug, product_slug):
#         try:
#             return Product.objects.filter(team__slug=team_slug).get(slug=product_slug)
#         except Product.DoesNotExist:
#             raise Http404
    
#     def get(self, request, team_slug, product_slug, format=None):
#         product = self.get_object(team_slug, product_slug)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)



class ProductDetailView(APIView):

    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CategoryView(APIView):

    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(team__name__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})
