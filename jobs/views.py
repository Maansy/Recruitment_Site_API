from .models import Job
from .serializers import JobSerializer, JobCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services.user_services import get_user

# Create your views here.

class JobView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        user = get_user(token)
        if not user:
            return Response({'message':'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        #git active jobs
        jobs = Job.objects.filter(company=user.company_id, is_active=True)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        token = request.COOKIES.get('jwt')
        user = get_user(token)
        if not user:
            return Response({'message':'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_interviewer:
            return Response({'message':'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        request.data['company'] = user.company_id
        serializer = JobCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message':'Bad request'}, status=status.HTTP_400_BAD_REQUEST)