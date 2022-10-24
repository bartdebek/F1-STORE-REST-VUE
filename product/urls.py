from django.urls import path, include

from .views import LatestProductsListView, TeamsListView, ProductDetailView, CategoryView, search

urlpatterns = [
    path('latest-products/', LatestProductsListView.as_view(), name='latest_products'),
    path('products/search/', search),
    path('teams/', TeamsListView.as_view(), name='teams_list'),
    path('products/<slug:category_slug>/<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<slug:category_slug>/', CategoryView.as_view(), name='category'),
]
