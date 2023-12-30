from django.db.models.signals import post_save
from django.dispatch import receiver
from readers.models import CustomUser
from django.core.mail import send_mail


@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
        "Welcome to BookTime!",
        f"Hello, {instance.username}! Welcome to BookTime. Enjoy the books and reviews",
        "bekhzodnabijonov@gmail.com",
        [instance.email]
    )
        