from django.urls import path
from .views import ApproveSellerView, SellerListByApprovalStatusView

urlpatterns = [
    path('sellers/<int:seller_id>/approve/', ApproveSellerView.as_view(), name='approve-seller'),
    path('sellers/', SellerListByApprovalStatusView.as_view(), name='seller-list-by-approval'),
]
