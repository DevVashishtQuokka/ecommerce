from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)
    
    def get_seller_by_id(self, seller_id):
        return self.filter(id=seller_id, user_type='seller').first()


    def approved_sellers(self):
        return self.filter(user_type='seller', is_approved=True)

    def unapproved_sellers(self):
        return self.filter(user_type='seller', is_approved=False)

    def all_buyers(self):
        return self.filter(user_type='buyer')
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    )

    username = None 
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_approved = models.BooleanField(default=False)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'user_type']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


User = get_user_model()


class AddressManager(models.Manager):
    def for_user(self, user):
        return self.filter(user=user)

    def in_city(self, city):
        return self.filter(city__iexact=city)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    objects = AddressManager() 

    def __str__(self):
        return f"{self.street}, {self.city}"

class PasswordResetOTPManager(models.Manager):
    def latest_for_user(self, user):
        return self.filter(user=user).order_by('-created_at').first()

    def is_valid_otp(self, user, otp):
        return self.filter(user=user, otp=otp).exists()


class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PasswordResetOTPManager() 


