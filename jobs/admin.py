from django.contrib import admin

# Register your models here.

from .models import Job

class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'company', 'created_at', 'updated_at', 'is_active']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['title', 'description', 'company']

admin.site.register(Job, JobAdmin)