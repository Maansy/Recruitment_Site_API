from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User
import jwt, datetime
from decouple import config

# from .models import User
# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serialzer = UserSerializer(data=request.data)
        serialzer.is_valid(raise_exception=True)
        serialzer.save()
        return Response(serialzer.data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        
        if user is None:
            return Response({'message':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response({'message':'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        secret = config('JWT_SECRET_KEY')
        token = jwt.encode(payload,secret,algorithm="HS256")
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        
        response.data = {
            'message':'Login successful', 
          'token': token
        }
        response.status_code = status.HTTP_200_OK
        return response
               
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
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'success'
        }
        response.status_code = status.HTTP_200_OK
        return response