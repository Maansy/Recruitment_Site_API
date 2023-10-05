from django.urls import path
from .views import JobView, JobDetailView,JobsView, JobApplicationView


urlpatterns = [
    path('', JobView.as_view(), name='job-list'),
    path('<int:job_id>/', JobDetailView.as_view(), name='job-detail'),
    path('all/', JobsView.as_view(), name='jobs-list'),
    path('applications/', JobApplicationView.as_view(), name='job-applications'),

]
