from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone
from datetime import datetime, timedelta

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


class CryptoData(models.Model):
    limit = models.IntegerField()
    offset = models.IntegerField()
    data = models.JSONField()
    total_items = models.IntegerField(default=0)
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['limit', 'offset']

class CryptoStateData(models.Model):
    type = models.CharField(max_length=255)
    data = models.JSONField()
    last_updated = models.DateTimeField(default=timezone.now)
    class Meta:
        unique_together = ['type']

class CoinDetail(models.Model):
    coin_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    description = models.TextField()
    icon_url = models.URLField()
    tier = models.IntegerField()
    rank = models.IntegerField()
    price = models.FloatField()
    btc_price = models.FloatField()
    price_at = models.DateTimeField()
    number_of_markets = models.IntegerField()
    number_of_exchanges = models.IntegerField()
    volume_24h = models.FloatField()
    market_cap = models.FloatField()
    fully_diluted_market_cap = models.FloatField()
    change = models.FloatField()
    all_time_high_price = models.FloatField()
    all_time_high_timestamp = models.DateTimeField()
    last_updated = models.DateTimeField(default=timezone.now)
    website_url = models.URLField()

    def save(self, *args, **kwargs):
        # Convert timestamps to datetime objects before saving
        self.price_at = datetime.strptime(self.price_at, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        self.all_time_high_timestamp = datetime.strptime(self.all_time_high_timestamp, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        super().save(*args, **kwargs)
