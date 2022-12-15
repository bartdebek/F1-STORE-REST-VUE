from django.urls import path, include

from .views import (
    LatestProductsListView, 
    TeamsProductsView, 
    TeamsListView, 
    TeamsProductsView, 
    ProductDetailView, 
    CategoryView, 
    search, 
    ReviewList,
    ReviewDetail
)

urlpatterns = [
    path('latest-products/', LatestProductsListView.as_view(), name='latest-products'),
    path('products/search/', search, name='search'),
    path('products/teams/', TeamsListView.as_view(), name='teams-list'),
    path('products/teams/<slug:team_slug>/', TeamsProductsView.as_view(), name='team-products'),
    path('products/<slug:category_slug>/<slug:product_slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<slug:category_slug>/', CategoryView.as_view(), name='category'),
    path('reviews/<slug:product_slug>/', ReviewList.as_view(), name='review-list'),
    path('reviews/detail/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
]
