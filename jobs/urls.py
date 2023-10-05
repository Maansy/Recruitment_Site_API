from django.urls import path
from .views import JobView, JobDetailView,JobsView, JobApplicationView,JobApplicationApplyView,JobApplicationsAnalysesView


urlpatterns = [
    path('', JobView.as_view(), name='job-list'),
    path('<int:job_id>/', JobDetailView.as_view(), name='job-detail'),
    path('all/', JobsView.as_view(), name='jobs-list'),
    path('<int:company_id>/applications/', JobApplicationView.as_view(), name='job-applications'),
    path('<int:company_id>/applications/<int:job_id>/', JobApplicationApplyView.as_view(), name='job-application'),
    path('<int:company_id>/applications/analyses/', JobApplicationsAnalysesView.as_view(), name='job-application-analyses'),
]
