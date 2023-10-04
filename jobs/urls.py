from django.urls import path
from .views import JobView, JobDetailView


urlpatterns = [
    path('', JobView.as_view(), name='job-list'),
    path('<int:pk>/', JobDetailView.as_view(), name='job-detail')
]
