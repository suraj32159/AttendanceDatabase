from django.contrib import admin
from .models import User
from .models import User_attendance_details

# Register your models here.

@admin.register(User)
@admin.register(User_attendance_details)

class DefaultAdmin(admin.ModelAdmin):
    pass
