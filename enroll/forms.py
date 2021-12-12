from django import forms
from .models import User
from django.core import validators 


class StudentRegistration(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name','course','enrollment_no','file_name']
        Course_Choice = [('mca','MCA'),('msc','M.Sc')]
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            #'course' : forms.ChoiceField(label='Select your course',widget=forms.CheckboxSelectMultiple(choices=Course_Choice)),
            #'course': forms.MultipleChoiceField(choices=Course_Choice,initial='0',widget=forms.SelectMultiple(),required=True,label='Select your course'),
            'course' : forms.Select(attrs={'class': 'form-control'}),
            'enrollment_no' : forms.NumberInput(attrs={'class': 'form-control'}),
            'file_name' : forms.ClearableFileInput(attrs={'multiple':'multiple','class':'form-control'})
        }