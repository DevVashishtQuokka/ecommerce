from django.urls import path
from .views import (
    CreateOrderView,
    OrderListView,
    OrderDetailView,
    CancelOrderView,
    AdminOrderStatusView
)

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='order-create'),
    path('my/', OrderListView.as_view(), name='my-orders'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('<int:pk>/cancel/', CancelOrderView.as_view(), name='cancel-order'),
    path('<int:pk>/status/', AdminOrderStatusView.as_view(), name='update-status'),
]
