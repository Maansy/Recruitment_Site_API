from rest_framework.response import Response
from rest_framework import status

class UserRegister:
    def __init__(self,serializer) -> None:
        self.serializer = serializer

    def create_user(self):
        self.serializer.is_valid(raise_exception=True)
        self.serializer.save()

    def get_response(self):
        self.create_user()
        return Response(self.serializer.data, status=status.HTTP_201_CREATED)
