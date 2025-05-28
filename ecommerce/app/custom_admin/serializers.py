from rest_framework import serializers
from app.user.models import CustomUser

class SellerListSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'business_name', 'is_approved', 'created_at']

class SellerApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'is_approved']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        instance.is_approved = True
        instance.save()
        return instance
