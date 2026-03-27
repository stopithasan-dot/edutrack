from django import forms
from .models import User
from academics.models import Subject

class AddTeacherForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select subjects this teacher will be responsible for."
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'profile_picture']

    def __init__(self, *args, **kwargs):
        self.institution = kwargs.pop('institution', None)
        super().__init__(*args, **kwargs)
        if self.institution:
            self.fields['subjects'].queryset = Subject.objects.filter(institution=self.institution)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.role = 'teacher'
        if commit:
            user.save()
            # Update the selected subjects to point to this new teacher
            for subject in self.cleaned_data.get('subjects', []):
                subject.teacher = user
                subject.save()
        return user

class AddStudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'class_ref', 'profile_picture']

    def __init__(self, *args, **kwargs):
        self.institution = kwargs.pop('institution', None)
        super().__init__(*args, **kwargs)
        if self.institution:
            from academics.models import Class
            self.fields['class_ref'].queryset = Class.objects.filter(institution=self.institution)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.role = 'student'
        if self.institution:
            user.institution = self.institution
        if commit:
            user.save()
        return user

class TeacherProfileUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to keep current password")
    
    class Meta:
        model = User
        fields = ['profile_picture', 'username', 'email', 'first_name', 'last_name', 'phone']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
