from django.shortcuts import render
from django.http import HttpResponse
from .forms import StudentRegistration
from django.core.files.storage import FileSystemStorage
from .models import User
from django.conf import settings
import os

# Create your views here.
def add_show(request):
	if request.method == 'POST':
		lis = []
		upload2 = request.POST.get("name")
		upload1 = request.POST.get("file_name")
		for f in request.FILES.getlist('file_name'):
			User(name = request.POST.get('name'),enrollment_no = request.POST.get('enrollment_no'),file_name=f).save()
			#lis.append(str(f))
		# file = ",". join(lis)
		# reg = User(name=request.POST.get('name'),enrollment_no=request.POST.get('enrollment_no'),file_name=file)
		# reg.save()
	
	fm = StudentRegistration()
	return render(request,'enroll/addandshow.html',{'form':fm})

def show(request):
	return HttpResponse('successfully uploaded')

'''
def upload(request):
    img = request.FILES['avatar']
    img_extension = os.path.splitext(img.name)[1]

    user_folder = 'static/profile/' + str(request.session['user_id'])
    if not os.path.exists(user_folder):
        os.mkdir(user_folder)

    img_save_path = "%s/%s%s" user_folder, 'avatar', img_extension
    with open(img_save_path, 'wb+') as f:
        for chunk in img.chunks():
            f.write(chunk)
'''

def success(request):
    return HttpResponse('successfully uploaded')
