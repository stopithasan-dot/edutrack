from django import forms
from .models import Notice

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['class_ref', 'title', 'message', 'is_active']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            if user.role == 'teacher':
                from academics.models import Subject
                from academics.models import Class
                subject_class_ids = Subject.objects.filter(teacher=user).values_list('class_ref', flat=True)
                self.fields['class_ref'].queryset = Class.objects.filter(id__in=subject_class_ids)
                self.fields['class_ref'].required = True
                self.fields['class_ref'].label = "Class"
            elif user.role in ['inst_admin', 'super_admin']:
                from academics.models import Class
                self.fields['class_ref'].queryset = Class.objects.filter(institution=user.institution)
                self.fields['class_ref'].required = False
                self.fields['class_ref'].empty_label = "Institution-Wide (All Classes)"
