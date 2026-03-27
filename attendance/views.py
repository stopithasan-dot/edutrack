from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from django.contrib import messages
from accounts.mixins import TeacherMixin
from academics.models import Class, Subject
from accounts.models import User
from .models import Attendance
from .forms import AttendanceFilterForm
from accounts.mixins import StudentMixin
from .utils import get_cumulative_attendance, calculate_attendance_percentage, LOW_ATTENDANCE_THRESHOLD
from django.http import HttpResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class StudentProfileTeacherView(TeacherMixin, DetailView):
    model = User
    template_name = 'attendance/student_profile_teacher.html'
    context_object_name = 'student'

    def get_queryset(self):
        return User.objects.filter(role='student', institution=self.request.user.institution)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        context['overall_attendance'] = get_cumulative_attendance(student)
        
        subjects = Subject.objects.filter(class_ref=student.class_ref)
        subject_stats = []
        for subject in subjects:
            percent = calculate_attendance_percentage(student, subject)
            subject_stats.append({
                'subject': subject.name,
                'percent': percent,
                'color': 'success' if percent >= 75 else ('warning' if percent >= 65 else 'danger')
            })
        context['subject_stats'] = subject_stats
        return context

class StudentReportPDFView(TeacherMixin, View):
    def get(self, request, pk):
        student = User.objects.filter(id=pk, role='student', institution=request.user.institution).first()
        if not student:
            return HttpResponse("Student not found", status=404)

        overall_attendance = get_cumulative_attendance(student)
        
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setFont("Helvetica-Bold", 18)
        p.drawString(100, 750, f"Academic Performance Report")
        
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 710, f"Student Information")
        p.setFont("Helvetica", 12)
        p.drawString(100, 690, f"Name: {student.get_full_name()}")
        p.drawString(100, 670, f"Class: {student.class_ref.name} {student.class_ref.section or ''}")
        p.drawString(100, 650, f"Email: {student.email}")
        
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 610, f"Attendance Summary")
        p.setFont("Helvetica", 12)
        p.drawString(100, 590, f"Overall Cumulative Attendance: {overall_attendance}%")
        
        p.drawString(100, 550, "Subject Attendance Breakdown:")
        
        y = 530
        subjects = Subject.objects.filter(class_ref=student.class_ref)
        for subject in subjects:
            percent = calculate_attendance_percentage(student, subject)
            p.drawString(120, y, f"- {subject.name}: {percent}%")
            y -= 25
            
        p.setFont("Helvetica-Oblique", 10)
        p.drawString(100, 100, f"Generated automatically by EduTrack for {request.user.institution.name}")
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Attendance_Report_{student.username}.pdf"'
        return response

class TeacherDashboardView(TeacherMixin, View):
    def get(self, request):
        teacher = request.user
        
        # Get unique classes the teacher teaches
        teacher_classes_data = []
        unique_classes = Class.objects.filter(
            subject__teacher=teacher, 
            institution=teacher.institution
        ).distinct()
        
        for cls in unique_classes:
            students = User.objects.filter(
                role='student', 
                class_ref=cls, 
                institution=teacher.institution
            ).order_by('first_name')
            
            student_data = []
            for st in students:
                percent = get_cumulative_attendance(st)
                student_data.append({
                    'student': st,
                    'percent': percent,
                    'color': 'success' if percent >= 75 else ('warning' if percent >= 65 else 'danger')
                })
            
            teacher_classes_data.append({
                'class': cls,
                'students': student_data,
                'total_students': students.count()
            })
            
        return render(request, 'dashboard/teacher_dashboard.html', {
            'teacher_classes_data': teacher_classes_data
        })

class MarkAttendanceView(TeacherMixin, View):
    def get(self, request):
        teacher = request.user
        form = AttendanceFilterForm(request.GET or None, teacher=teacher)
        students = None
        subject = None
        date = request.GET.get('date')

        if form.is_valid():
            subject = form.cleaned_data['subject']
            class_ref = form.cleaned_data['class_ref']
            
            already_marked = Attendance.objects.filter(subject=subject, date=date).exists()
            if already_marked:
                messages.warning(request, "Attendance for this subject and date is already marked.")
                return redirect('attendance_edit')
            
            students = User.objects.filter(role='student', class_ref=class_ref, institution=teacher.institution)
            
        return render(request, 'attendance/mark.html', {
            'form': form,
            'students': students,
            'subject': subject,
            'date': date
        })

    def post(self, request):
        teacher = request.user
        subject_id = request.POST.get('subject_id')
        date = request.POST.get('date')
        
        if not subject_id or not date:
            messages.error(request, "Invalid submission.")
            return redirect('attendance_mark')
            
        subject = Subject.objects.get(id=subject_id)
        students = User.objects.filter(role='student', class_ref=subject.class_ref, institution=teacher.institution)
        
        for student in students:
            status = request.POST.get(f'student_{student.id}', 'absent')
            Attendance.objects.create(
                institution=teacher.institution,
                subject=subject,
                student=student,
                date=date,
                status=status,
                marked_by=teacher
            )
            
        messages.success(request, f"Attendance marked for {subject.name} on {date}.")
        return redirect('teacher_dashboard')

class EditAttendanceView(TeacherMixin, View):
    def get(self, request):
        teacher = request.user
        form = AttendanceFilterForm(request.GET or None, teacher=teacher)
        attendances = None
        subject = None
        date = request.GET.get('date')

        if form.is_valid():
            subject = form.cleaned_data['subject']
            attendances = Attendance.objects.filter(subject=subject, date=date, marked_by=teacher)
            
        return render(request, 'attendance/edit.html', {
            'form': form,
            'attendances': attendances,
            'subject': subject,
            'date': date
        })

    def post(self, request):
        teacher = request.user
        subject_id = request.POST.get('subject_id')
        date = request.POST.get('date')
        
        if not subject_id or not date:
            messages.error(request, "Invalid submission.")
            return redirect('attendance_edit')
            
        subject = Subject.objects.get(id=subject_id)
        attendances = Attendance.objects.filter(subject=subject, date=date, marked_by=teacher)
        
        for record in attendances:
            status = request.POST.get(f'attendance_{record.id}')
            if status in dict(Attendance.STATUS_CHOICES).keys():
                record.status = status
                record.save()
                
        messages.success(request, "Attendance updated successfully.")
        return redirect('teacher_dashboard')

class StudentDashboardView(StudentMixin, View):
    def get(self, request):
        student = request.user
        cumulative = get_cumulative_attendance(student)
        show_warning = cumulative < LOW_ATTENDANCE_THRESHOLD and cumulative > 0
        
        subjects = Subject.objects.filter(class_ref=student.class_ref)
        subject_stats = []
        for subject in subjects:
            percent = calculate_attendance_percentage(student, subject)
            color = 'success' if percent >= 75 else ('warning' if percent >= 65 else 'danger')
            subject_stats.append({
                'subject': subject,
                'percent': percent,
                'color': color
            })
            
        return render(request, 'dashboard/student_dashboard.html', {
            'cumulative': cumulative,
            'show_warning': show_warning,
            'subject_stats': subject_stats,
            'threshold': LOW_ATTENDANCE_THRESHOLD,
        })
