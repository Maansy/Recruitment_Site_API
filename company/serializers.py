from rest_framework import serializers
from .models import Company
from users.models import User

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
    #         name = models.CharField(max_length=100)
    # location = models.CharField(max_length=100)
    # logo = models.ImageField(upload_to='company/images/')
    # description = models.TextField()
    # employee_count = models.IntegerField()
    # Linkedin = models.URLField()
    # website = models.URLField()
    # facebook = models.URLField()
    # twitter = models.URLField()
    # is_active = models.BooleanField(default=True)
        model = Company
        fields = ['name', 'location', 'logo', 'description', 'employee_count', 'Linkedin', 'website', 'facebook', 'twitter', 'is_active']
