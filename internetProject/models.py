from django.db import models


# Create your models here.
class Currency_rate(models.Model):
    from_currency = models.CharField(max_length=3)
    to_currency = models.CharField(max_length=3)
    rate = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_currency} to {self.to_currency} rate is {self.rate} at {self.time}"

# For the payment
class Payment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    card_number = models.CharField(max_length=16)
    card_expiry_month = models.CharField(max_length=2)
    card_expiry_year = models.CharField(max_length=4)
    card_cvc = models.CharField(max_length=3)
    # Add other payment-related fields as needed

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.card_number} - {self.card_expiry_month}/{self.card_expiry_year}'
