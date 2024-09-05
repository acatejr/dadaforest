from django.urls import path
from .views import AssetSearchResults, AssetDetailView

urlpatterns = [
    path("", AssetSearchResults.as_view(), name="asset_search_results"),
    path("assets/<int:pk>/", AssetDetailView.as_view(), name="asset-detail"),
]
