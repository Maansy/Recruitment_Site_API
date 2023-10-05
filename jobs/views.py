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
    
class JobDetailView(APIView):
    def get(self,request,job_id):
        token = request.COOKIES.get('jwt')
        user = get_user(token)
        if not user:
            return Response({'message':'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        job = Job.objects.filter(id=job_id, company=user.company_id).first()
        if not job:
            return Response({'message':'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = JobSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self,request,job_id):
        token = request.COOKIES.get('jwt')
        user = get_user(token)
        if not user:
            return Response({'message':'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        job = Job.objects.filter(id=job_id, company=user.company_id).first()
        if not job:
            return Response({'message':'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        if user.is_interviewer:
            return Response({'message':'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        request.data['company'] = user.company_id
        serializer = JobCreateSerializer(job, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message':'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,job_id):
        token = request.COOKIES.get('jwt')
        user = get_user(token)
        if not user:
            return Response({'message':'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        job = Job.objects.filter(id=job_id, company=user.company_id).first()
        if not job:
            return Response({'message':'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        if user.is_interviewer:
            return Response({'message':'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        job.delete()
        return Response({'message':'Job deleted'}, status=status.HTTP_200_OK)
    

class JobsView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        #git active jobs
        jobs = Job.objects.filter(is_active=True)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)