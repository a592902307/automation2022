from django.contrib import admin
from sgin import models
# Register your models here.
admin.site.register(models.Event)
admin.site.register(models.Guest)
admin.site.register(models.GuestEvent)