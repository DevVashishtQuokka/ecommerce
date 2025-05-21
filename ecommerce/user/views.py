from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .serializers import UserSerializer, PasswordResetSerializer, ResetPasswordSerializer, AddressSerializer, UserProfileSerializer
from django.core.mail import send_mail
from utils.responder import standard_response
from rest_framework.views import APIView
from rest_framework import status
#from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Address
from utils.responder import Responder 

User = get_user_model()
def get_object_or_none(model, **kwargs):
    return model.objects.filter(**kwargs).first()

class UserListCreateAPIView(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
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
            return Responder.error_response(400)
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Responder.success_response(102, data=None)


class PasswordResetRequestView(APIView):

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = get_object_or_none(User, email=email)

        if not user:
            return standard_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="User with this email does not exist.",
                data=None
            )

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://localhost:8000/reset-password/{uid}/{token}/"
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email]
        )
        return standard_response(
            status_code=status.HTTP_200_OK,
            message="Password reset link sent to your email.",
            data=None
        )


class ResetPasswordConfirmView(APIView):

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data['password']
        token = serializer.validated_data['token']
        uid = serializer.validated_data['uid']

        user = get_object_or_none(User, pk=urlsafe_base64_decode(uid).decode())
        if not user:
            return standard_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="User does not exist.",
                data=None
            )

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return standard_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Invalid token.",
                data=None
            )

        user.set_password(password)
        user.save()
        return standard_response(
            status_code=status.HTTP_200_OK,
            message="Password reset successfully.",
            data=None
        )


class UserProfileView(APIView):
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return standard_response(
            status_code=status.HTTP_200_OK,
            message="User profile fetched successfully.",
            data=serializer.data
        )
    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return standard_response(
            status_code=status.HTTP_200_OK,
            message="User profile updated successfully.",
            data=serializer.data
        )


class AddressListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return standard_response(
            status_code=status.HTTP_200_OK,
            message="Address list fetched successfully.",
            data=serializer.data
        )

    def post(self, request):
        serializer = AddressSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return standard_response(
            status_code=status.HTTP_201_CREATED,
            message="Address created successfully.",
            data=serializer.data
        )


class AddressDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        address = get_object_or_none(Address, pk=pk, user=request.user)
        if not address:
            return standard_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Address not found.",
                data=None
            )
        serializer = AddressSerializer(address)
        return standard_response(
            status_code=status.HTTP_200_OK,
            message="Address fetched successfully.",
            data=serializer.data
        )

    def put(self, request, pk):
        address = get_object_or_none(Address, pk=pk, user=request.user)
        if not address:
            return standard_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Address not found.",
                data=None
            )
        serializer = AddressSerializer(address, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return standard_response(
            status_code=status.HTTP_200_OK,
            message="Address updated successfully.",
            data=serializer.data
        )

    def delete(self, request, pk):
        address = get_object_or_none(Address, pk=pk, user=request.user)
        if not address:
            return standard_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Address not found.",
                data=None
            )
        address.delete()
        return standard_response(
            status_code=status.HTTP_204_NO_CONTENT,
            message="Address deleted successfully.",
            data=None
        )
