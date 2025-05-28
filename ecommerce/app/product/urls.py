from django.urls import path
from .views import ProductCategoryView, ItemListCreateView, ItemDetailView

urlpatterns = [
    path('categories/', ProductCategoryView.as_view(), name='product-categories'),
    path('', ItemListCreateView.as_view(), name='item-list-create'),
    path('<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
]

