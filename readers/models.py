from django.db import models
from django.contrib.auth.models import AbstractUser


class Readers(AbstractUser):
    class Status(models.TextChoices):
        New = "New", "New"
        Active = "Active", "Active"

    picture = models.ImageField(default='profile_pictures/anonim_user.png', upload_to='profile_pictures/')
    address = models.CharField(max_length=300, blank=True, default="")
    phone = models.CharField(max_length=13)
    balance = models.DecimalField(max_digits=8, decimal_places=2, blank=True, default=0)
    status = models.CharField(max_length=6,
                              choices=Status.choices,
                              default=Status.New
                              )
    
    class Meta:
        verbose_name = 'Reader'
        verbose_name_plural = 'Readers'
        

class Payment(models.Model):
    reader = models.ForeignKey(Readers, related_name='payment_reader', on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_update_date = models.DateTimeField(auto_now=True)
    payment_edited = models.BooleanField(default=False)
    payee = models.ForeignKey(Readers, related_name='payment_payee', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.reader.first_name} {self.reader.last_name} ({self.payment_amount}) to'ladi"
    