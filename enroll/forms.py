from django import forms
from .models import User
from .models import User_attendance_details
from django.core import validators 


class StudentRegistration(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name','course','enrollment_no','file_name']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'course' : forms.Select(attrs={'class': 'form-control'}),
            'enrollment_no' : forms.NumberInput(attrs={'class': 'form-control'}),
            'file_name' : forms.ClearableFileInput(attrs={'multiple':'multiple','class':'form-control','accept':'image/png, image/gif, image/jpeg'})
        }


class TeachersAttendanceRegistration(forms.ModelForm):
    class Meta:
        model = User_attendance_details
        fields = ['teachers_name','subject','course','sem','batch_year']
        widgets = {
            'teachers_name' : forms.TextInput(attrs={'class':'form-control'}),
            'subject' : forms.Select(attrs={'class': 'form-control'}),
            'course' : forms.Select(attrs={'class': 'form-control'}),
            'sem' : forms.Select(attrs={'class': 'form-control'}),
            'batch_year' : forms.Select(attrs={'class': 'form-control'})
        }