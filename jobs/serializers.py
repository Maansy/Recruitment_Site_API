from .models import Job
from rest_framework import serializers
from company.models import Company

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        extra_kwargs = {'company': {'required': True}}

    def validate_company(self, company):
        if company:
            if not Company.objects.filter(id=company.id).exists():
                raise serializers.ValidationError('Company not found')
        return company

    def create(self, validated_data):
        return Job.objects.create(**validated_data)