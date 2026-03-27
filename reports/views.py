from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from .utils import generate_student_report

class DownloadReportView(LoginRequiredMixin, View):
    def get(self, request, student_id=None):
        if request.user.role == 'student':
            student = request.user
        else:
            student = User.objects.get(id=student_id, institution=request.user.institution)
            
        pdf_buffer = generate_student_report(student)
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Attendance_Report_{student.username}.pdf"'
        return response
