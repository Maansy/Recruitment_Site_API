
from rest_framework.response import Response
from rest_framework import status

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