from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import CartItem
from .serializers import (
    CartItemSerializer,
    CartItemAddUpdateSerializer,
    CartItemRemoveSerializer
)
from utils.responder import Responder


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = CartItem.objects.filter(cart__user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Responder.success_response(code=166, data=serializer.data)

    def post(self, request):
        serializer = CartItemAddUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            cart_item = serializer.create_or_update(user=request.user)
            return Responder.success_response(code=167, data=CartItemSerializer(cart_item).data, status_code=201)
        return Responder.error_response(code=168, errors=serializer.errors)

    def patch(self, request):
        serializer = CartItemAddUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            cart_item = serializer.create_or_update(user=request.user)
            return Responder.success_response(code=169, data=CartItemSerializer(cart_item).data)
        return Responder.error_response(code=170, errors=serializer.errors)

    def delete(self, request):
        serializer = CartItemRemoveSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            CartItem.objects.filter(cart__user=request.user, product_id=product_id).delete()
            return Responder.success_response(code=171, data={"removed": True}, status_code=202)
        return Responder.error_response(code=172, errors=serializer.errors)
