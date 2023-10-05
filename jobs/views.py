from .models import Job, JobApplication
from .serializers import JobSerializer, JobCreateSerializer, JobApplicationSerializer
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
        jobs = Job.objects.filter(is_active=True)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class JobApplicationView(APIView):
    def get(self,request, company_id):
        token = request.COOKIES.get('jwt')
        user = get_user(token)
        if not user:
            return Response({'message':'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_interviewer:
            applications = JobApplication.objects.filter(job__company=company_id)
            serializer = JobApplicationSerializer(applications, many=True)
        else:
            applications = JobApplication.objects.filter(job__company=user.company_id)
            serializer = JobApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class JobApplicationApplyView(APIView):
    def post(self,request,company_id,job_id):
        token = request.COOKIES.get('jwt')
        user = get_user(token)
        if not user:
            return Response({'message':'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_interviewer:
            job = Job.objects.filter(id=job_id, company=company_id).first()
            if not job:
                return Response({'message':'Job not found'}, status=status.HTTP_404_NOT_FOUND)
            if not job.is_active:
                return Response({'message':'Job not active'}, status=status.HTTP_400_BAD_REQUEST)
            application = JobApplication.objects.filter(job=job, candidate=user).first()
            if application:
                return Response({'message':'Already applied'}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        linkedin_url = data.get('linkedin_url')
        github_url = data.get('github_url')
        application = JobApplication.objects.create(job=job, candidate=user, linkedin_url=linkedin_url, github_url=github_url)
        serializer = JobApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self,request,company_id,job_id):
        token = request.COOKIES.get('jwt')
        user = get_user(token)
        if not user:
            return Response({'message':'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_interviewer:
            application = JobApplication.objects.filter(job__company=company_id, job=job_id, status='pending').first()
        else:
            application = JobApplication.objects.filter(job__company=user.company_id, job=job_id, candidate=user).first()
        if not application:
            return Response({'message':'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = JobApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)

class JobApplicationsAnalysesView(APIView):
    def get(self,request,company_id):
        token = request.COOKIES.get('jwt')
        user = get_user(token)
        if not user:
            return Response({'message':'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_interviewer:
            return Response({'message':'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        applications = JobApplication.objects.filter(job__company=company_id)
        applications_count = applications.count()
        accepted_count = applications.filter(status='accepted').count()
        rejected_count = applications.filter(status='rejected').count()
        pending_count = applications.filter(status='pending').count()
        return Response({
            'applications_count': applications_count,
            'accepted_count': accepted_count,
            'rejected_count': rejected_count,
            'pending_count': pending_count,
        }, status=status.HTTP_200_OK)