from django.http import Http404
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError

from .models import Category, Product, Team, Review
from .serializers import ProductSerializer, TeamSerializer, CategorySerializer, ReviewSerializer
from .permissions import IsReviewUserOrReadOnly, IsAdmin


class LatestProductsListView(APIView):
    """
    Display a list of 4 latest :model:`product.Product` instances.

    **Context**

    ``products``
        A list of 4 latest :model:`product.Product` instances.

    **Serializer**

    ``ProductSerializer``
    """
    @method_decorator(cache_page(60*60*2))
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class TeamsListView(APIView):
    """
    Display a list of instances :model:`product.Team`

    **Context**

    ``teams``
        A list of instances :model:`product.Team`.

    **Serializer**

    ``TeamSerializer``
    """
    @method_decorator(cache_page(60*60*2))
    def get(self, request, format=None):
        teams = Team.objects.order_by('name')
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)


class TeamsProductsView(APIView):
    """
    Display a list of instances :model:`product.Product`
    related to specific :model:`product.Team`.

    **Context**

    ``products``
        Display a list of instances :model:`product.Product`
        related to specific :model:`product.Team`.

    **Serializer**

    ``ProductSerializer``
    """
    @method_decorator(cache_page(60*60*2))
    def get(self, request, team_slug, format=None):
        products = Product.objects.filter(team__slug=team_slug)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    """
    Display an individual :model:`product.Product`.

    **Context**

    ``product``
        An instance of :model:`product.Product`.

    **Serializer**

    ``ProductSerializer``
    """
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    @method_decorator(cache_page(60*60*2))
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CategoryView(APIView):
    """
    Display a list of instances :model:`product.Product`
    related to specific :model:`product.Category`.

    **Context**

    ``category``
        A list of instances :model:`product.Product`
        related to specific :model:`product.Category`.

    **Serializer**

    ``CategorySerializer``
    """
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Product.DoesNotExist:
            raise Http404

    @method_decorator(cache_page(60*60*2))
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


@api_view(['POST'])
def search(request):
    """
    Post a keyword query and get related instances of
    :model:`product.Product`.

    **query**

    ``products``
        A list of instances :model:`product.Product`
        containing posted keyoword (in name or
        any relation).

    **Serializer**

    ``ProductSerializer``
    """
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(team__name__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})


class ReviewList(generics.ListCreateAPIView):
    """
    POST method: Create an instance of :model:`product.Review`
    related to specific instance of :model:`product.Product`.

    GET method: Display list of :model:`product.Review` instances
    related to specific instance of :model:`product.Product`.

    **query**

    ``reviews``
        A list of instances of :model:`product.Review`
        related to specific :mode:`product.Product`.

    **Serializer**

    ``ReviewSerializer``
    """
    serializer_class = ReviewSerializer
    model = Review

    def get_queryset(self):
        product_slug = self.kwargs['product_slug']
        queryset = Review.objects.filter(product__slug=product_slug)
        return queryset

    def perform_create(self, serializer):
        product_slug = self.kwargs['product_slug']
        product = Product.objects.get(slug=product_slug)
        author = self.request.user
        review_queryset = Review.objects.filter(product=product, author=author)

        if review_queryset.exists():
            raise ValidationError("You have already added a review!")

        serializer.save(product=product, author=author)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    PUT method: Update an instance of :model:`product.Review`.

    GET method: Display instance of :model:`product.Review`.

    DELETE method: Delete instance of :model:`product.Review`.

    **query**

    ``review``
        An instance of :model:`product.Review`.

    **Serializer**

    ``ReviewSerializer``
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsAdmin)

    def get_object(self):
        pk = self.kwargs['pk']
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        pk = self.kwargs['pk']
        review = self.get_object(pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
