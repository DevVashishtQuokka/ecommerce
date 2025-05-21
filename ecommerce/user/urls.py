from django.urls import path
from .views import ( 
    UserListCreateAPIView, LogoutAPIView,PasswordResetRequestAPIView , PasswordResetConfirmAPIView ,UserProfileAPIView
    , AddressListCreateAPIView , AddressRetrieveUpdateDestroyAPIView
)
urlpatterns = [
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('password-reset/', PasswordResetRequestAPIView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('addresses/', AddressListCreateAPIView.as_view(), name='address-list-create'),
    path('addresses/<int:pk>/', AddressRetrieveUpdateDestroyAPIView.as_view(), name='address-detail'),
]

