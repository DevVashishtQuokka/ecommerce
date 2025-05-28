from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
from app.product.models import Item

User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.email}"


class CartItemManager(models.Manager):
    def create_or_update(self, user, product, quantity):
        cart, _ = Cart.objects.get_or_create(user=user)
        cart_item, created = self.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        return cart_item


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    Product = models.ForeignKey(Item,on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    objects = CartItemManager()

    class Meta:
        unique_together = ('cart', 'Product')

    def __str__(self):
        return f"{self.product.name} x {self.quantity} in cart of {self.cart.user.email}"


