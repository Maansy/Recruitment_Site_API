from django.shortcuts import render
from .models import Company
from .serializers import CompanySerializer 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decouple import config
import jwt
from users.models import User
# Create your views here.

class CompanyView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            return Response({'message':'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            secret = config('JWT_SECRET_KEY')
            payload = jwt.decode(token, secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return Response({'message':'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.filter(id=payload['id']).first()
        if not user:
            return Response({'message':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if user.is_interviewer:
            serializer = CompanySerializer(Company.objects.all(), many=True)
            return Response(serializer.data)
        if not user.company:
            return Response({'message':'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CompanySerializer(user.company)
        return Response(serializer.data)