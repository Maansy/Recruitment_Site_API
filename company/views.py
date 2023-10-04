from rest_framework.views import APIView
from rest_framework.response import Response
from services.user_services import get_user
from services.company_services import check_user_privilage

class CompanyView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        user = get_user(token)
        serializer = check_user_privilage(user)
        return Response(serializer.data)