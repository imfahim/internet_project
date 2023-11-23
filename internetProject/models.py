from django.db import models


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
