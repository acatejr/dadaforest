from django.urls import path
from .views import AssetSearchResults, AssetDetailView, MapSearchView

urlpatterns = [
    path("", AssetSearchResults.as_view(), name="asset_search_results"),
    path("assets/<int:pk>/", AssetDetailView.as_view(), name="asset-detail"),
    path("map/", MapSearchView.as_view(), name="map-search"),
]
