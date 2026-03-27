from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.role == 'super_admin':
            return '/admin/'
        elif user.role == 'inst_admin':
            return reverse_lazy('inst_dashboard')
        elif user.role == 'teacher':
            return reverse_lazy('teacher_dashboard')
        elif user.role == 'student':
            return reverse_lazy('student_dashboard')
        return '/'

def logout_view(request):
    logout(request)
    return redirect('landing_page')

def redirect_by_role(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    if user.role == 'super_admin':
        return redirect('/admin/')
    elif user.role == 'inst_admin':
        return redirect('inst_dashboard')
    elif user.role == 'teacher':
        return redirect('teacher_dashboard')
    elif user.role == 'student':
        return redirect('student_dashboard')
    return redirect('landing_page')

from django.views.generic import UpdateView
from .forms import TeacherProfileUpdateForm
from .mixins import TeacherMixin

class TeacherProfileView(TeacherMixin, UpdateView):
    form_class = TeacherProfileUpdateForm
    template_name = 'accounts/teacher_profile.html'
    success_url = reverse_lazy('teacher_profile_edit')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        from django.contrib import messages
        from django.contrib.auth import update_session_auth_hash
        user = form.save()
        if form.cleaned_data.get('password'):
            update_session_auth_hash(self.request, user)
        messages.success(self.request, 'Your profile was updated successfully!')
        return super().form_valid(form)
