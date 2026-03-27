from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.redirect_by_role, name='dashboard_redirect'),
    path('dashboard/teacher/profile/', views.TeacherProfileView.as_view(), name='teacher_profile_edit'),
]
