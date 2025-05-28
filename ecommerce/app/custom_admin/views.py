from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.core.mail import send_mail
from django.conf import settings
from utils.responder import Responder
from app.user.models import CustomUser
from .serializers import SellerListSerializer, SellerApprovalSerializer


class SellerListByApprovalStatusView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        approved_sellers = CustomUser.objects.approved_sellers()
        pending_sellers = CustomUser.objects.unapproved_sellers()

        approved_data = SellerListSerializer(approved_sellers, many=True).data
        pending_data = SellerListSerializer(pending_sellers, many=True).data

        data = {
            "approved_sellers": approved_data,
            "pending_sellers": pending_data,
        }
        return Responder.success_response(200, data=data)


class ApproveSellerView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, seller_id):
        seller = CustomUser.objects.get_seller_by_id(seller_id)

        if not seller:
            return Responder.error_response(404, errors={"error": "Seller profile not found."})

        if seller.is_approved:
            return Responder.error_response(400, errors={"error": "Seller already approved."})

        serializer = SellerApprovalSerializer(seller, data={'is_approved': True}, partial=True)
        if serializer.is_valid():
            serializer.save()

            send_mail(
                subject="Seller Account Approved",
                message="Congratulations! Your seller account has been approved. You can now add products.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[seller.email],
            )

            return Responder.success_response(200, data=serializer.data)

        return Responder.error_response(400, errors={"error": "Validation failed."})
