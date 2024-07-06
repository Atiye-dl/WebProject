
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .views import send_invoice_email

@receiver(post_save, sender=Order)
def send_invoice_on_order_complete(sender, instance, created, **kwargs):
    if created:
        send_invoice_email(instance)
