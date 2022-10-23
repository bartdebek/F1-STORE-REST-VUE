from django.urls import path, include

from .views import LatestProductsList, TeamsList

urlpatterns = [
    path('latest-products/', LatestProductsList.as_view(), name='latest_products'),
    path('teams/', TeamsList.as_view(), name='teams_list'),
]
