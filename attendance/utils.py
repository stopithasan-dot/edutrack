from .models import Attendance

LOW_ATTENDANCE_THRESHOLD = 75

def calculate_attendance_percentage(student, subject):
    total_classes = Attendance.objects.filter(subject=subject, student=student).count()
    present_classes = Attendance.objects.filter(subject=subject, student=student, status='present').count()
    if total_classes == 0:
        return 0
    return round((present_classes / total_classes) * 100, 2)

def get_cumulative_attendance(student):
    all_records = Attendance.objects.filter(student=student)
    total = all_records.count()
    present = all_records.filter(status='present').count()
    if total == 0:
        return 0
    return round((present / total) * 100, 2)

def get_monthly_attendance(student, subject, month, year):
    return Attendance.objects.filter(
        student=student,
        subject=subject,
        date__month=month,
        date__year=year
    )
