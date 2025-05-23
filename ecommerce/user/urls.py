from django.urls import path
from .views import (
    UserListCreateAPIView, LogoutView, PasswordResetRequestView, 
    ResetPasswordConfirmView, UserProfileView, 
    AddressListCreateAPIView, AddressDetailAPIView, LoginView
)

urlpatterns = [
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/', ResetPasswordConfirmView.as_view(), name='password-reset-confirm'),  
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('addresses/', AddressListCreateAPIView.as_view(), name='address-list-create'),
    path('addresses/<int:pk>/', AddressDetailAPIView.as_view(), name='address-detail'),

]
