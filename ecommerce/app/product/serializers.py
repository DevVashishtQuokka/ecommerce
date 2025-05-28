from rest_framework import serializers
from .models import ProductCategory, Item, ItemImage

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'
        read_only_fields = ['slug']

class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ['id', 'image', 'is_featured']

class ItemSerializer(serializers.ModelSerializer):
    item_images = ItemImageSerializer(many=True, required=False)

    class Meta:
        model = Item
        fields = ['id', 'seller', 'title', 'description', 'cost', 'available_stock', 'category', 'brand_name', 'item_images']
        read_only_fields = ['id', 'seller']

    def create(self, validated_data):
        images = validated_data.pop('item_images', [])
        item = Item.objects.create(**validated_data)
        for img in images:
            ItemImage.objects.create(item=item, **img)
        return item

    def update(self, instance, validated_data):
        images = validated_data.pop('item_images', None)
        instance = super().update(instance, validated_data)
        if images is not None:
            instance.item_images.all().delete()
            for img in images:
                ItemImage.objects.create(item=instance, **img)
        return instance
