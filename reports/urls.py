from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/student/reports/download/', views.DownloadReportView.as_view(), name='download_report'),
    path('dashboard/teacher/reports/download/<int:student_id>/', views.DownloadReportView.as_view(), name='teacher_download_report'),
]
