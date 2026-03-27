from django.views.generic import CreateView, TemplateView, ListView
from django.urls import reverse_lazy
from .models import Institution
from accounts.models import User
from django import forms
from django.db import transaction
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from accounts.mixins import InstitutionAdminMixin
from academics.models import Class, Subject
from attendance.models import Attendance
from django.utils import timezone
from accounts.forms import AddTeacherForm, AddStudentForm
from academics.forms import ClassForm, SubjectForm

class InstitutionRegistrationForm(forms.ModelForm):
    admin_first_name = forms.CharField(max_length=150, required=True)
    admin_last_name = forms.CharField(max_length=150, required=True)
    admin_email = forms.EmailField(required=True)
    admin_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Institution
        fields = ['name', 'address', 'email', 'phone', 'slug']

    def clean_admin_email(self):
        email = self.cleaned_data.get('admin_email')
        if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
            raise forms.ValidationError("User with this email already exists.")
        return email

    @transaction.atomic
    def save(self, commit=True):
        institution = super().save(commit=True)
        # Create Institution Admin Account
        User.objects.create_user(
            username=self.cleaned_data['admin_email'],
            email=self.cleaned_data['admin_email'],
            password=self.cleaned_data['admin_password'],
            first_name=self.cleaned_data['admin_first_name'],
            last_name=self.cleaned_data['admin_last_name'],
            role='inst_admin',
            institution=institution
        )
        return institution

class InstitutionRegisterView(CreateView):
    template_name = 'institutions/register.html'
    form_class = InstitutionRegistrationForm
    success_url = reverse_lazy('login')

class AdminDashboardView(InstitutionAdminMixin, TemplateView):
    template_name = 'dashboard/admin_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        institution = self.request.user.institution
        context['total_teachers'] = User.objects.filter(institution=institution, role='teacher').count()
        context['total_students'] = User.objects.filter(institution=institution, role='student').count()
        context['total_classes'] = Class.objects.filter(institution=institution).count()
        
        today = timezone.now().date()
        today_att = Attendance.objects.filter(institution=institution, date=today)
        total_marked = today_att.count()
        total_present = today_att.filter(status='present').count()
        context['today_attendance_percent'] = round((total_present / total_marked) * 100, 2) if total_marked > 0 else 0
        
        return context

class TeacherListView(InstitutionAdminMixin, ListView):
    model = User
    template_name = 'institutions/teacher_list.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        return User.objects.filter(institution=self.request.user.institution, role='teacher')

class TeacherCreateView(InstitutionAdminMixin, CreateView):
    model = User
    form_class = AddTeacherForm
    template_name = 'institutions/teacher_form.html'
    success_url = reverse_lazy('teacher_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['institution'] = self.request.user.institution
        return kwargs

    def form_valid(self, form):
        form.instance.institution = self.request.user.institution
        return super().form_valid(form)

class TeacherUpdateView(InstitutionAdminMixin, UpdateView):
    model = User
    form_class = AddTeacherForm
    template_name = 'institutions/teacher_form.html'
    success_url = reverse_lazy('teacher_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['institution'] = self.request.user.institution
        return kwargs

class TeacherDeleteView(InstitutionAdminMixin, DeleteView):
    model = User
    template_name = 'institutions/confirm_delete.html'
    success_url = reverse_lazy('teacher_list')

    def get_queryset(self):
        return User.objects.filter(institution=self.request.user.institution, role='teacher')

class StudentListView(InstitutionAdminMixin, ListView):
    model = User
    template_name = 'institutions/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        return User.objects.filter(institution=self.request.user.institution, role='student')

class StudentCreateView(InstitutionAdminMixin, CreateView):
    model = User
    form_class = AddStudentForm
    template_name = 'institutions/student_form.html'
    success_url = reverse_lazy('student_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['institution'] = self.request.user.institution
        return kwargs

    def form_valid(self, form):
        form.instance.institution = self.request.user.institution
        return super().form_valid(form)

class StudentUpdateView(InstitutionAdminMixin, UpdateView):
    model = User
    form_class = AddStudentForm
    template_name = 'institutions/student_form.html'
    success_url = reverse_lazy('student_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['institution'] = self.request.user.institution
        return kwargs

class StudentDeleteView(InstitutionAdminMixin, DeleteView):
    model = User
    template_name = 'institutions/confirm_delete.html'
    success_url = reverse_lazy('student_list')

    def get_queryset(self):
        return User.objects.filter(institution=self.request.user.institution, role='student')

class ClassListView(InstitutionAdminMixin, ListView):
    model = Class
    template_name = 'institutions/class_list.html'
    context_object_name = 'classes'

    def get_queryset(self):
        return Class.objects.filter(institution=self.request.user.institution)

class ClassCreateView(InstitutionAdminMixin, CreateView):
    model = Class
    form_class = ClassForm
    template_name = 'institutions/class_form.html'
    success_url = reverse_lazy('class_list')

    def form_valid(self, form):
        form.instance.institution = self.request.user.institution
        return super().form_valid(form)

class ClassUpdateView(InstitutionAdminMixin, UpdateView):
    model = Class
    form_class = ClassForm
    template_name = 'institutions/class_form.html'
    success_url = reverse_lazy('class_list')

class ClassDeleteView(InstitutionAdminMixin, DeleteView):
    model = Class
    template_name = 'institutions/confirm_delete.html'
    success_url = reverse_lazy('class_list')

    def get_queryset(self):
        return Class.objects.filter(institution=self.request.user.institution)

class SubjectListView(InstitutionAdminMixin, ListView):
    model = Subject
    template_name = 'institutions/subject_list.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        return Subject.objects.filter(institution=self.request.user.institution)

class SubjectCreateView(InstitutionAdminMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'institutions/subject_form.html'
    success_url = reverse_lazy('subject_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['institution'] = self.request.user.institution
        return kwargs

    def form_valid(self, form):
        form.instance.institution = self.request.user.institution
        return super().form_valid(form)

class SubjectUpdateView(InstitutionAdminMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'institutions/subject_form.html'
    success_url = reverse_lazy('subject_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['institution'] = self.request.user.institution
        return kwargs

class SubjectDeleteView(InstitutionAdminMixin, DeleteView):
    model = Subject
    template_name = 'institutions/confirm_delete.html'
    success_url = reverse_lazy('subject_list')

    def get_queryset(self):
        return Subject.objects.filter(institution=self.request.user.institution)

class AdminAnalyticsView(InstitutionAdminMixin, TemplateView):
    template_name = 'institutions/analytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        institution = self.request.user.institution
        
        # Subject-wise attendance
        subjects = Subject.objects.filter(institution=institution)
        subject_names = []
        subject_percents = []
        
        for subject in subjects:
            total = Attendance.objects.filter(subject=subject).count()
            present = Attendance.objects.filter(subject=subject, status='present').count()
            percent = round((present / total) * 100, 2) if total > 0 else 0
            subject_names.append(subject.name)
            subject_percents.append(percent)
            
        context['subject_names'] = subject_names
        context['subject_percents'] = subject_percents
        
        # Leaderboard
        students = User.objects.filter(institution=institution, role='student')
        leaderboard = []
        for student in students:
            total = Attendance.objects.filter(student=student).count()
            present = Attendance.objects.filter(student=student, status='present').count()
            percent = round((present / total) * 100, 2) if total > 0 else 0
            leaderboard.append({'student': student, 'percent': percent})
            
        leaderboard.sort(key=lambda x: x['percent'], reverse=True)
        context['leaderboard'] = leaderboard[:10]
        
        # Monthly attendance trend data
        context['months'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        context['monthly_data'] = [85, 88, 86, 92, 90, 89]
        
        return context
