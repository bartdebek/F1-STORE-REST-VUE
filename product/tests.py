import secrets

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import force_authenticate, APIClient

from .models import Product, Team, Category, Review


class APITests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Setup data for mock profile creation.
        """
        cls.user = User.objects.create(
            id=1,
            username="testuser",
            password="testpassword"
        )
        cls.category = Category.objects.create(
            name="Clothing",
            slug="clothing"
        )
        cls.team = Team.objects.create(
            name="Torro Rosso",
            slug="torro-rosso"
        )
        cls.product = Product.objects.create(
            name="TestProduct",
            slug="test-product",
            category=cls.category,
            team=cls.team,
            price=50
        )
        cls.review = Review.objects.create(
            body="Test review",
            product=cls.product,
            author=User.objects.get(username='testuser')
        )

    def setUp(self):
        self.relative_path = '/api/v1/'

    def test_latest_product_exists_at_correct_location(self):
        response = self.client.get(reverse('latest-products'), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_teams_list_exists_at_correct_location(self):
        response = self.client.get(reverse('teams-list'), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_team_products_exists_at_correct_location(self):
        response = self.client.get(self.relative_path + 'products/clothing/')
        self.assertEqual(response.status_code, 200)

    def test_product_page_exists_at_correct_location(self):
        response = self.client.get(self.relative_path + 'products' + self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_review_page_exists_at_correct_location(self):
        response = self.client.get(self.relative_path + 'reviews/test-product/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['body'], "Test review")
