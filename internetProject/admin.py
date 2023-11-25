from django.contrib import admin

from internetProject.models import Complaint, Feedback, Payment

# Register your models here.
admin.site.register(Complaint)
admin.site.register(Feedback)

admin.site.register(Payment)