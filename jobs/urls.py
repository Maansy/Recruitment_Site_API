from django.urls import path
from .views import JobView


urlpatterns = [
    path('', JobView.as_view(), name='job-list')
]
