from rest_framework import serializers
from .models import BusinessDetail

class BusinessDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDetail
        fields = ['business_name', 'gst_number', 'website']

    def validate(self, attrs):
        user = self.context['request'].user
        method = self.context.get('method', 'POST')

        if user.user_type != 'seller':
            raise serializers.ValidationError("Only sellers can add business details.")
        if not user.is_approved:
            raise serializers.ValidationError("Your seller account is not approved yet.")

        if method == 'POST' and BusinessDetail.objects.filter(user=user).exists():
            raise serializers.ValidationError("Business details have already been submitted.")

        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
