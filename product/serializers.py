from rest_framework import serializers

from .models import Category, Team, Product, Review


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "get_absolute_url",
            "description",
            "price",
            "get_image",
            "get_thumbnail"
        ]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "get_absolute_url",
            "get_image",
            "get_thumbnail",
        ]


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "products",
            "get_absolute_url",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    time = serializers.DateTimeField(source="created_on", format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = Review
        fields = [
            "id",
            "body",
            "author",
            "author_name",
            "product",
            "product_name",
            "time"
        ]
        read_only_fields = ['author', 'product']
