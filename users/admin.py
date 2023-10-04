from django.contrib import admin

# Register your models here.
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('email','name','is_staff','is_active','is_manager','is_employee','is_interviewer','company')
    list_filter = ('is_staff','is_active','is_manager','is_employee','is_interviewer','company')
    search_fields = ('email','name')
    ordering = ('email',)

admin.site.register(User, UserAdmin)