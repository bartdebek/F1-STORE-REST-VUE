from rest_framework import serializers

from .models import Category, Team, Product


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
    # products = ProductSerializer(many=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            # "products",
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