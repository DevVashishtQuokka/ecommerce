from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from utils.helper import get_object_or_none
from utils.responder import Responder
from .serializers import BusinessDetailSerializer
from .models import BusinessDetail

class BusinessDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        business_detail = get_object_or_none(BusinessDetail, user=request.user)
        if not business_detail:
            return Responder.error(408, errors={"error": "Business details not found."})

        serializer = BusinessDetailSerializer(business_detail)
        return Responder.success(113, data=serializer.data)

    def post(self, request):
        if BusinessDetail.objects.filter(user=request.user).exists():
            return Responder.error(409, errors={"error": "Business details already exist."})

        serializer = BusinessDetailSerializer(
            data=request.data,
            context={'request': request, 'method': 'POST'}
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Responder.success(115, data=serializer.data, http_status=status.HTTP_201_CREATED)
        return Responder.error(400, errors=serializer.errors)

    def patch(self, request):
        business_detail = get_object_or_none(BusinessDetail, user=request.user)
        if not business_detail:
            return Responder.error(408, errors={"error": "Business details not found."})

        serializer = BusinessDetailSerializer(
            business_detail,
            data=request.data,
            partial=True,
            context={'request': request, 'method': 'PATCH'}
        )
        if serializer.is_valid():
            serializer.save()
            return Responder.success(114, data=serializer.data)
        return Responder.error(400, errors=serializer.errors)
