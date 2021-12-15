from django import forms
from .models import User
from django.core import validators 


class StudentRegistration(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name','course','semester','enrollment_no','file_name']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'course' : forms.Select(attrs={'class': 'form-control'}),
            'semester' : forms.Select(attrs={'class':'form-control'}),
            'enrollment_no' : forms.NumberInput(attrs={'class': 'form-control'}),
            'file_name' : forms.ClearableFileInput(attrs={'multiple':'multiple','class':'form-control','accept':'image/png, image/gif, image/jpeg'})
        }