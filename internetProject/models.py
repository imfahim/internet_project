from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class Currency_rate(models.Model):
    from_currency = models.CharField(max_length=3)
    to_currency = models.CharField(max_length=3)
    rate = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_currency} to {self.to_currency} rate is {self.rate} at {self.time}"


class Complaint(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='complaint_attachments/', blank=True, null=True)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.title


class Feedback(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# For the payment
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    given_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    create_time = models.DateTimeField()
    email_address = models.EmailField()
    payer_id = models.CharField(max_length=255)
    reference_id = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    currency_code = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.status} - {self.create_time} - {self.given_name} {self.surname} - {self.email_address} - {self.payer_id} - {self.reference_id} - {self.value} {self.currency_code}"


