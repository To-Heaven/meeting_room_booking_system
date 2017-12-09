from django.contrib import admin

from room import models


admin.site.register(models.MeetingRoom)
admin.site.register(models.User)
admin.site.register(models.Order)
