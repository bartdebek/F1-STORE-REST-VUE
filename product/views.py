from django.http import Http404
from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework import status

from .models import Category, Product, Team, Review
from .serializers import ProductSerializer, TeamSerializer, CategorySerializer, ReviewSerializer


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


class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    model = Review

    def get(self, request, product_slug):
        queryset = Review.objects.filter(product__slug=product_slug)
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    # def post(self, request, *args, **kwargs):
    #     serializer = ReviewSerializer(data=request.data)
    #     return self.create(request, *args, **kwargs)

    def perform_create(self, serialize, product_slug):
        product = Product.objects.get(slug=product_slug)
        serializer = ReviewSerializer(product)
        author = self.request.user
        review_queryset = Review.objects.filter(product=product, author=author)

        if review_queryset.exists():
            raise ValidationError("This user has already added a review!")

        serializer.save(product=product, author=author)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer