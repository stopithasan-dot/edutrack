from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/teacher/', views.TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('dashboard/teacher/student/<int:pk>/', views.StudentProfileTeacherView.as_view(), name='student_profile_teacher'),
    path('dashboard/teacher/student/<int:pk>/report/', views.StudentReportPDFView.as_view(), name='student_report_pdf'),
    path('dashboard/teacher/attendance/mark/', views.MarkAttendanceView.as_view(), name='attendance_mark'),
    path('dashboard/teacher/attendance/edit/', views.EditAttendanceView.as_view(), name='attendance_edit'),
    path('dashboard/student/', views.StudentDashboardView.as_view(), name='student_dashboard'),
]
