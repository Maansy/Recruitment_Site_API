
from company.serializers import CompanySerializer 
from rest_framework.response import Response
from company.models import Company
from rest_framework import status


def check_user_privilage(user):
    if not user:
        return Response({'message':'User not found'}, status=status.HTTP_404_NOT_FOUND)
    if user.is_interviewer:
        serializer = CompanySerializer(Company.objects.all(), many=True)
        return Response(serializer.data)
    if not user.company:
        return Response({'message':'Company not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CompanySerializer(user.company)
    return serializer