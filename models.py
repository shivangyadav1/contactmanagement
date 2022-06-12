from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Data(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    companyName = models.CharField(max_length=200, null=True, blank=True)
    product = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        order_with_respect_to = 'user'
