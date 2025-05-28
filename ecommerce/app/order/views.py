from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from utils.responder import Responder
from .models import Order
from app.cart.models import CartItem
from .serializers import OrderSerializer
from .permissions import IsOrderOwner

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_items = CartItem.objects.filter(cart__user=request.user)
        if not cart_items.exists():
            return Responder.error_response(1001, "Your cart is empty.")

        items_data = [
            {"product": item.product, "quantity": item.quantity}
            for item in cart_items
        ]

        try:
            order = Order.objects.create_with_items(request.user, items_data)
            cart_items.delete()
        except ValueError as e:
            return Responder.error_response(1002, str(e))

        return Responder.success_response(1003, OrderSerializer(order).data, status_code=201)

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.user_orders(request.user)
        return Responder.success_response(1004, OrderSerializer(orders, many=True).data)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOrderOwner]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        self.check_object_permissions(request, order)
        return Responder.success_response(1005, OrderSerializer(order).data)

class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated, IsOrderOwner]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        self.check_object_permissions(request, order)
        try:
            updated = Order.objects.cancel(order)
        except ValueError as e:
            return Responder.error_response(1006, str(e))
        return Responder.success_response(1007, OrderSerializer(updated).data)

class AdminOrderStatusView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, pk):
        action = request.data.get("action")
        order = get_object_or_404(Order, pk=pk)

        try:
            if action == "ship":
                order = Order.objects.ship(order)
            elif action == "deliver":
                order = Order.objects.deliver(order)
            else:
                return Responder.error_response(1008, "Invalid action.")
        except ValueError as e:
            return Responder.error_response(1009, str(e))

        return Responder.success_response(1010, OrderSerializer(order).data)