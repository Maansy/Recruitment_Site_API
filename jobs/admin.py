from django.contrib import admin

# Register your models here.

from .models import Job, JobApplication

class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'company', 'created_at', 'updated_at', 'is_active']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['title', 'description', 'company']

admin.site.register(Job, JobAdmin)

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['job', 'candidate', 'created_at', 'updated_at', 'status']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['job', 'candidate']

admin.site.register(JobApplication, JobApplicationAdmin)