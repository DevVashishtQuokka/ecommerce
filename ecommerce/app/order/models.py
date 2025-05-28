from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from app.product.models import Item

User = get_user_model()

class OrderManager(models.Manager):
    def create_with_items(self, user, items_data):
        total = 0
        order_items = []

        for item in items_data:
            product = item['product']
            qty = item['quantity']

            if product.stock < qty:
                raise ValueError(f"Insufficient stock for {product.name}")

            total += product.price * qty
            order_items.append((product, qty, product.price))

        order = self.create(user=user, total_amount=total)

        for product, qty, price in order_items:
            product.stock -= qty
            product.save()
            OrderItem.objects.create(order=order, product=product, quantity=qty, price=price)

        return order

    def user_orders(self, user):
        return self.filter(user=user).order_by('-created_at')

    def cancel(self, order):
        if order.status != 'pending':
            raise ValueError("Only pending orders can be cancelled.")

        order.status = 'cancelled'
        order.save()

        for item in order.items.all():
            item.product.stock += item.quantity
            item.product.save()

        return order

    def ship(self, order):
        if order.status != 'pending':
            raise ValueError("Only pending orders can be shipped.")
        order.status = 'shipped'
        order.shipped_at = timezone.now()
        order.save()
        return order

    def deliver(self, order):
        if order.status != 'shipped':
            raise ValueError("Only shipped orders can be delivered.")
        order.status = 'delivered'
        order.delivered_at = timezone.now()
        order.save()
        return order

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    objects = OrderManager()

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"