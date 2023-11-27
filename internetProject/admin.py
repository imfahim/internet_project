from django.contrib import admin

from internetProject.models import Complaint, Feedback, Currency_rate, Payment, UserProfile

# Register your models here.
admin.site.register(Complaint)
admin.site.register(Feedback)
admin.site.register(Currency_rate)
admin.site.register(Payment)
admin.site.register(UserProfile)
