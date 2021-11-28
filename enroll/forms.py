from django import forms
from .models import User
from django.core import validators 


class StudentRegistration(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name','enrollment_no','file_name']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'enrollment_no' : forms.NumberInput(attrs={'class': 'form-control'}),
            'file_name' : forms.ClearableFileInput(attrs={'multiple':'multiple','class':'form-control'})
        }