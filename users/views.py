from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User
import jwt, datetime
from decouple import config
from services.user_login_services import UserLoginService
from services.user_regsiter_services import UserRegister
from services.user_services import logout
# from .models import User
# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        user_service = UserRegister(serializer)
        return user_service.get_response()

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user_service = UserLoginService(email, password)
        return user_service.get_response()
               
class UserView(APIView):
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
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class LogoutView(APIView):
    def post(self, request):
        response = logout()
        return response