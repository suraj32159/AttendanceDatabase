from django.shortcuts import render
from django.http import HttpResponse
from .forms import StudentRegistration
from django.core.files.storage import FileSystemStorage
from .models import User
from django.conf import settings
from django.contrib import messages
import os
import sys
import cv2
import pickle
import numpy as np
from deepface import DeepFace
from retinaface import RetinaFace

# Create your views here.
def add_show(request):
	if request.method == 'POST':
		for f in request.FILES.getlist('file_name'):
			User(name = request.POST.get('name'),course=request.POST.get('course'),semester=request.POST.get('semester'),enrollment_no = request.POST.get('enrollment_no'),file_name=f).save()
		messages.success(request, 'Form submission successful')
	
		#save_path = settings.MEDIA_ROOT +"/"+str(request.POST.get('course')) 
		save_path="../media/"+str(request.POST.get('course'))+"/" +str(request.POST.get('name'))
		findencodings(request.POST.get('name'),request.POST.get('course'),request.POST.get('semester'))
		#return HttpResponse(save_path)
	# Find encodings
	# folder call"
	# findencodings(request.POST.get('name'),request.POST.get('course'))
	# append in exist file if not exist create

	fm = StudentRegistration()
	return render(request,'enroll/addandshow.html',{'form':fm})


def findencodings(Sname,course,sem):
	MODEL = 'Facenet'
	known_faces = []
	known_names = []
	path=settings.MEDIA_ROOT+"/"+str(course)+"/"+str(sem)
	for name in os.listdir(path):
		myDict=[]
		for imgName in os.listdir(path+"/"+name):
			image = cv2.imread(f'{path}/{name}/{imgName}')
			encoding = DeepFace.represent(image,model_name=MODEL,model=DeepFace.build_model(MODEL),enforce_detection=False,detector_backend='retinaface',align=True,normalization='base')
			myDict.append(encoding)
		known_faces.append(myDict)
		known_names.append(name)

		save_path = settings.MEDIA_ROOT+"/Encodings/"+str(course)+'/'+str(sem)+'/known_faces'
		save_encods = open(save_path,"wb")
		pickle.dump(known_faces,save_encods)
		pickle.dump(known_names,save_encods)
		save_encods.close()

def success(request):
    return HttpResponse('successfully uploaded')
