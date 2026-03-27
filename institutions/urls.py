from django.urls import path
from . import views

urlpatterns = [
    path('register/institution/', views.InstitutionRegisterView.as_view(), name='institution_register'),
    path('dashboard/admin/', views.AdminDashboardView.as_view(), name='inst_dashboard'),
    path('dashboard/admin/teachers/', views.TeacherListView.as_view(), name='teacher_list'),
    path('dashboard/admin/teachers/add/', views.TeacherCreateView.as_view(), name='teacher_add'),
    path('dashboard/admin/teachers/<int:pk>/edit/', views.TeacherUpdateView.as_view(), name='teacher_edit'),
    path('dashboard/admin/teachers/<int:pk>/delete/', views.TeacherDeleteView.as_view(), name='teacher_delete'),
    path('dashboard/admin/students/', views.StudentListView.as_view(), name='student_list'),
    path('dashboard/admin/students/add/', views.StudentCreateView.as_view(), name='student_add'),
    path('dashboard/admin/students/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_edit'),
    path('dashboard/admin/students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),
    path('dashboard/admin/classes/', views.ClassListView.as_view(), name='class_list'),
    path('dashboard/admin/classes/add/', views.ClassCreateView.as_view(), name='class_add'),
    path('dashboard/admin/classes/<int:pk>/edit/', views.ClassUpdateView.as_view(), name='class_edit'),
    path('dashboard/admin/classes/<int:pk>/delete/', views.ClassDeleteView.as_view(), name='class_delete'),
    path('dashboard/admin/subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('dashboard/admin/subjects/add/', views.SubjectCreateView.as_view(), name='subject_add'),
    path('dashboard/admin/subjects/<int:pk>/edit/', views.SubjectUpdateView.as_view(), name='subject_edit'),
    path('dashboard/admin/subjects/<int:pk>/delete/', views.SubjectDeleteView.as_view(), name='subject_delete'),
    path('dashboard/admin/reports/', views.AdminAnalyticsView.as_view(), name='admin_reports'),
]
