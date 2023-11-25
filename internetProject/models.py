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
# class Payment(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     card_number = models.CharField(max_length=16)
#     card_expiry_month = models.CharField(max_length=2)
#     card_expiry_year = models.CharField(max_length=4)
#     card_cvc = models.CharField(max_length=3)
#     # Add other payment-related fields as needed
#
#     def __str__(self):
#         return f'{self.first_name} {self.last_name} - {self.card_number} - {self.card_expiry_month}/{self.card_expiry_year}'





class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16)
    id_number = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_id}"
