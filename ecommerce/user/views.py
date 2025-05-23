from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from utils.responder import Responder
from utils.otpgen import generate_otp
from .serializers import (
    UserProfileSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    AddressSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer,
)

User = get_user_model()

def get_object_or_none(model, **kwargs):
    return model.objects.filter(**kwargs).first()

class UserListCreateAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        users = User.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Responder.success_response(100, data=serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responder.success_response(101, data=serializer.data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Responder.error_response(400, message="Refresh token not provided.")
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Responder.success_response(102, data=None)
        except Exception:
            return Responder.error_response(403, message="Invalid or expired token.")



class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = get_object_or_none(User, email=email)

        if not user:
            return Responder.error_response(401, message="User not found.")

        otp = generate_otp()
        cache.set(f'otp_{email}', otp, timeout=300)

        send_mail(
            subject="Your OTP for Password Reset",
            message=f"Use this OTP to reset your password: {otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return Responder.success_response(103, data={"message": "OTP sent to email"})


class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']

        user = get_object_or_none(User, email=email)
        if not user:
            return Responder.error_response(405, message="User not found.")

        cached_otp = cache.get(f'otp_{email}')
        if cached_otp != otp:
            return Responder.error_response(404, message="Invalid OTP.")

        user.set_password(new_password)
        user.save()
        cache.delete(f'otp_{email}')

        return Responder.success_response(104, data={"message": "Password reset successful"})


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Responder.success_response(105, data=serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responder.success_response(106, data=serializer.data)



class AddressListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Responder.success_response(107, data=serializer.data)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Responder.success_response(108, data=serializer.data)


# -
class AddressDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        address = get_object_or_none(Address, pk=pk, user=request.user)
        if not address:
            return Responder.error_response(402, message="Address not found.")
        serializer = AddressSerializer(address)
        return Responder.success_response(109, data=serializer.data)

    def put(self, request, pk):
        address = get_object_or_none(Address, pk=pk, user=request.user)
        if not address:
            return Responder.error_response(402, message="Address not found.")
        serializer = AddressSerializer(address, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responder.success_response(110, data=serializer.data)

    def delete(self, request, pk):
        address = get_object_or_none(Address, pk=pk, user=request.user)
        if not address:
            return Responder.error_response(402, message="Address not found.")
        address.delete()
        return Responder.success_response(111, data=None)
    
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer