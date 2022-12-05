from django.urls import path, include

from .views import (
    LatestProductsListView, 
    TeamsProductsView, 
    TeamsListView, 
    TeamsProductsView, 
    ProductDetailView, 
    CategoryView, 
    search, 
    ReviewList
)

urlpatterns = [
    path('latest-products/', LatestProductsListView.as_view(), name='latest_products'),
    path('products/search/', search),
    path('products/teams/', TeamsListView.as_view(), name='teams_list'),
    path('products/teams/<slug:team_slug>/', TeamsProductsView.as_view(), name='team_products'),
    path('reviews/<slug:product_slug>/', ReviewList.as_view(), name='review-list'),
    path('products/<slug:category_slug>/<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<slug:category_slug>/', CategoryView.as_view(), name='category'),
]
