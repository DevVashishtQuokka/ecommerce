from rest_framework import serializers
from .models import Cart, CartItem
from app.product.models import Item
from app.product.serializers import ItemSerializer
from utils.responder import Responder


class CartItemSerializer(serializers.ModelSerializer):
    product = ItemSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='items', many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']


class CartItemAddUpdateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        if not Item.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product with this ID does not exist.")
        return value

    def validate(self, attrs):
        product = Item.objects.get(id=attrs['product_id'])
        if product.stock < attrs['quantity']:
            raise serializers.ValidationError("Requested quantity exceeds available stock.")
        return attrs

    def create_or_update(self, user):
        product = Item.objects.get(id=self.validated_data['product_id'])
        quantity = self.validated_data['quantity']
        return CartItem.objects.create_or_update(user=user, product=product, quantity=quantity)


class CartItemRemoveSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Item.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product ID.")
        return value
