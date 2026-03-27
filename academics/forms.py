from django import forms
from .models import Class, Subject

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'section']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['class_ref', 'name', 'code', 'credits', 'teacher']

    def __init__(self, *args, **kwargs):
        institution = kwargs.pop('institution', None)
        super().__init__(*args, **kwargs)
        if institution:
            self.fields['class_ref'].queryset = Class.objects.filter(institution=institution)
            from accounts.models import User
            self.fields['teacher'].queryset = User.objects.filter(institution=institution, role='teacher')
