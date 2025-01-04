from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.InboxMessage)
admin.site.register(models.Conversation)