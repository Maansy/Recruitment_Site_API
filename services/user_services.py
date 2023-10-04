
from rest_framework.response import Response
from rest_framework import status
from decouple import config
import jwt
from users.models import User


def logout() -> Response:
    """
    Logout user by deleting the jwt cookie
    """
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message':'success'
    }
    response.status_code = status.HTTP_200_OK
    return response

def get_user(token) -> User:
    """
    Get user from jwt token
    """
    if not token:
        return Response({'message':'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        secret = config('JWT_SECRET_KEY')
        payload = jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return Response({'message':'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
    user = User.objects.filter(id=payload['id']).first()
    return user