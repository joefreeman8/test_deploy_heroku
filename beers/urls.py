from django.urls import path 
from .views import BeerListView, BeerDetailView

urlpatterns = [
    path('', BeerListView.as_view()),
    path('<int:pk>/', BeerDetailView.as_view())
]