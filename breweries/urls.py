from django.urls import path 
from .views import BreweryListView, BreweryDetailView

urlpatterns = [
    path('', BreweryListView.as_view()),
    path('<int:pk>/', BreweryDetailView.as_view()),
]