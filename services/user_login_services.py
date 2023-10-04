from rest_framework import status
from rest_framework.response import Response
from users.models import User
import jwt, datetime
from decouple import config

class UserLoginService:
    def __init__(self,email, password) -> None:
        self.email = email
        self.password = password

    def get_user(self):
        return User.objects.filter(email=self.email).first()
    
    def check_user(self):
        user = self.get_user()
        if user is None:
            return Response({'message':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(self.password):
            return Response({'message':'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
        return user
    
    def get_token(self):
        user = self.check_user()
        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        secret = config('JWT_SECRET_KEY')
        token = jwt.encode(payload,secret,algorithm="HS256")
        return token
    
    def get_response(self):
        token = self.get_token()
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'message':'Login successful', 
            'token': token
        }
        response.status_code = status.HTTP_200_OK
        return response
    

