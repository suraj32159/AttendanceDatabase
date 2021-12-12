from django.shortcuts import render
from django.http import HttpResponse
from .forms import StudentRegistration
from django.core.files.storage import FileSystemStorage
from .models import User
from django.conf import settings
from django.contrib import messages
import os

# Create your views here.
def add_show(request):
	if request.method == 'POST':
		for f in request.FILES.getlist('file_name'):
			User(name = request.POST.get('name'),course=request.POST.get('course'),enrollment_no = request.POST.get('enrollment_no'),file_name=f).save()
		messages.success(request, 'Form submission successful')
	
	# Find encodings
	# folder call
	# append in exist file if not exist create

	fm = StudentRegistration()
	return render(request,'enroll/addandshow.html',{'form':fm})


def success(request):
    return HttpResponse('successfully uploaded')
