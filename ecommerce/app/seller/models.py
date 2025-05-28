from django.db import models
from app.user.models import CustomUser

# Create your models here.
class BusinessDetail(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=15)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.business_name}"
