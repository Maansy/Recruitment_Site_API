from django.contrib import admin
from .models import Company

# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name','location','employee_count','Linkedin','website','facebook','twitter', 'is_active')
    list_filter = ('name','location','employee_count')
    search_fields = ('name','location')
    ordering = ('name',)

admin.site.register(Company, CompanyAdmin)