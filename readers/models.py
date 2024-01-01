from django.db import models
from django.contrib.auth.models import AbstractUser


class Readers(AbstractUser):
    class Status(models.TextChoices):
        New = "NW", "New"
        Active = "AC", "Active"

    picture = models.ImageField(default='profile_pictures/anonim_user.png', upload_to='profile_pictures/')
    address = models.CharField(max_length=300, blank=True, default="")
    phone = models.CharField(max_length=13)
    balance = models.DecimalField(max_digits=8, decimal_places=2, blank=True, default=0)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.New
                              )
    
    class Meta:
        verbose_name = 'Reader'
        verbose_name_plural = 'Readers'
        