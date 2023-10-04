from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from services.user_login_services import UserLoginService
from services.user_regsiter_services import UserRegister
from services.user_services import logout, get_user

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
        user = get_user(token)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class LogoutView(APIView):
    def post(self, request):
        response = logout()
        return response