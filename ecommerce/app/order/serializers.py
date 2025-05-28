from rest_framework import serializers
from .models import Order, OrderItem
from app.product.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']

class OrderCreateItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        try:
            product = Product.objects.get(id=data['product_id'])
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found.")

        if product.stock < data['quantity']:
            raise serializers.ValidationError(f"Not enough stock for {product.name}")

        data['product'] = product
        return data

class OrderCreateSerializer(serializers.Serializer):
    items = OrderCreateItemSerializer(many=True)

    def validate(self, data):
        if not data['items']:
            raise serializers.ValidationError("Order must contain at least one item.")
        return data

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'updated_at', 'status', 'total_amount', 'items']
        read_only_fields = ['user', 'created_at', 'updated_at', 'total_amount']