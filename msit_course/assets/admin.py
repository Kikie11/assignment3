from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Asset, MaintenanceLog

admin.site.register(User, UserAdmin)
admin.site.register(Asset)
admin.site.register(MaintenanceLog)