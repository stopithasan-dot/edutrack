from django import forms
from academics.models import Class, Subject
from .models import Attendance

class AttendanceFilterForm(forms.Form):
    class_ref = forms.ModelChoiceField(queryset=Class.objects.none(), label="Class")
    subject = forms.ModelChoiceField(queryset=Subject.objects.none(), label="Subject")
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher:
            subjects = Subject.objects.filter(teacher=teacher)
            self.fields['subject'].queryset = subjects
            class_ids = subjects.values_list('class_ref', flat=True).distinct()
            self.fields['class_ref'].queryset = Class.objects.filter(id__in=class_ids)

# We won't use a strict Django Form for marking, as it's dynamic based on students in the class.
# We will handle it manually in the view using POST data.
