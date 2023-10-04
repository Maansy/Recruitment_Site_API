from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name','is_staff','is_active','is_manager','is_employee','is_interviewer','company', 'password']
        read_only_fields = ['is_staff','is_active','is_manager','is_employee','is_interviewer','company']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
