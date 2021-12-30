from django.shortcuts import render
from django.http import HttpResponse
from .forms import StudentRegistration
from .forms import TeachersAttendanceRegistration
from django.core.files.storage import FileSystemStorage
from .models import User
from .models import User_attendance_details
from django.conf import settings
from django.contrib import messages
import os
import sys
import cv2
import pickle
import numpy as np
from deepface import DeepFace
from retinaface import RetinaFace
from datetime import date

import csv
import os
import sys
import cv2
import numpy as np
from deepface import DeepFace
from retinaface import RetinaFace
import random
import pickle
from os.path import exists

# Create your views here.
def add_show(request):
	if request.method == 'POST':
		for f in request.FILES.getlist('file_name'):
			User(name = request.POST.get('name'),course=request.POST.get('course'),enrollment_no = request.POST.get('enrollment_no'),file_name=f).save()
		messages.success(request, 'Form submission successful')
	
		#save_path = settings.MEDIA_ROOT +"/"+str(request.POST.get('course')) 
		save_path="../media/"+str(request.POST.get('course'))+"/" +str(request.POST.get('name'))
		findencodings(request.POST.get('name'),request.POST.get('course'))
		return HttpResponse(save_path)

	fm = StudentRegistration()
	return render(request,'enroll/addandshow.html',{'form':fm})

def genrate_report(request):
	userAttendance = User_attendance_details.objects.all()
	return render(request,'enroll/report.html',{'details':userAttendance})

def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['Teachers Name', 'Students Name', 'Subject', 'Course','Semester','Batch Year','Date'])
    users = User_attendance_details.objects.all().values_list('teachers_name', 'student_name', 'subject', 'course','sem','batch_year','date')
    for user in users:
        writer.writerow(user)

    return response

    return response

def findencodings(Sname,course):
	MODEL = 'Facenet'
	known_faces = []
	known_names = []
	path = settings.MEDIA_ROOT+"/"+str(course)
	save_path_encodings = settings.MEDIA_ROOT+"/Encodings/"+str(course)+".dat"
	save_path_names = settings.MEDIA_ROOT+"/Encodings/"+str(course)+'_names.dat'

	file_exists = exists(save_path_names)
	if file_exists:
		# Load face encodings
		with open(save_path_encodings, 'rb') as f:
			known_faces = pickle.load(f)
		# Load name
		with open(save_path_names, 'rb') as f:
			known_names = pickle.load(f)
		if Sname in known_names:
			pass
		else:
			known_names,known_faces = getEncodings(Sname,MODEL,path,known_faces,known_names)
	else:
		known_names,known_faces = getEncodings(Sname,MODEL,path,known_faces,known_names)

	with open(save_path_encodings, 'wb') as f:
		pickle.dump(known_faces, f)
	with open(save_path_names, 'wb') as f:
	    pickle.dump(known_names, f)

def getEncodings(Sname,MODEL,path,known_faces,known_names):
	myDict=[]
	for imgName in os.listdir(path+"/"+Sname):
		image = cv2.imread(f'{path}/{Sname}/{imgName}')
		encoding = DeepFace.represent(image,model_name=MODEL,model=DeepFace.build_model(MODEL),enforce_detection=False,detector_backend='retinaface',align=True,normalization='base')
		myDict.append(encoding)
	known_faces.append(myDict)
	known_names.append(Sname)

	return known_names,known_faces


def success(request):
    return HttpResponse('successfully uploaded')


def teachers_home(request):
	if request.method == 'POST':
		RegisterAttendance(request)
		# return HttpResponse('successfully uploaded')


	fm = TeachersAttendanceRegistration()
	return render(request,'enroll/teachers_home.html',{'form':fm})

def l2_normalize(x):
	return x / np.sqrt(np.sum(np.multiply(x, x)))

def findCosineDistance(source_representation, test_representation , tolerance):
  data = ""
  distAll =[]
  for i in source_representation:
    dist = []
    for j in i:
      a = np.matmul(np.transpose(j), test_representation)
      b = np.sum(np.multiply(j, j))
      c = np.sum(np.multiply(test_representation, test_representation))
      data = 1 - (a / (np.sqrt(b) * np.sqrt(c)))
      dist.append(data)
    minValue = min(dist)
    # distAll.append((minValue)<=tolerance)
    distAll.append(minValue)
  
  minData = min(distAll)
  if minData <= tolerance:
    index = distAll.index(minData)
    distAll[index] = True
  return distAll

def findEuclideanDistance(source_representation, test_representation,tolerance=0.9):
  distAll =[]
  for i in source_representation:
    dist = []
    for j in i:
        if type(j) == list:
            j = l2_normalize(np.array(j))
        if type(test_representation) == list:
            test_representation = l2_normalize(np.array(test_representation))

        euclidean_distance = j - test_representation
        euclidean_distance = np.sum(np.multiply(euclidean_distance, euclidean_distance))
        euclidean_distance = (np.sqrt(euclidean_distance))
        dist.append(euclidean_distance)
    minValue = min(dist)
    # distAll.append(minValue)
    distAll.append((minValue)<=tolerance)
  return distAll

def name_to_color(name):
  #g,y,w,o
    listData = [[57, 255, 20],[250,237,39],[39,237,250],[0, 0, 255],[31, 95, 255]]
    color = random.choice(listData)
    # color = [(ord(c.lower())-97)*8 for c in name[:3]]
    return color

# Function to mark attendance
def markAttendance(name,request):
	today = date.today()
	teachers_name = request.POST.get('teachers_name')
	subject=request.POST.get('subject')
	course = request.POST.get('course')
	sem = request.POST.get('sem')
	batch_year=request.POST.get('course')
	userAttendance = User_attendance_details.objects.get(teachers_name=teachers_name,student_name=name,subject=subject,course=course,sem=sem,batch_year=batch_year,date=today)

	# if len(userAttendance) == 0:
	User_attendance_details(teachers_name=teachers_name,student_name=name,subject=subject,course=course,sem=sem,batch_year=batch_year,date=today).save()

	return True

def registerAttendance(request):
	teachers_name = request.POST.get('teachers_name')
	subject=request.POST.get('subject')
	course = request.POST.get('course')
	sem = request.POST.get('sem')
	batch_year=request.POST.get('course')

	videoPath = settings.MEDIA_ROOT+"/VideoDemo/output.avi"
	path_encodings = settings.MEDIA_ROOT+"/Encodings/"+str(course)+".dat"
	path_names = settings.MEDIA_ROOT+"/Encodings/"+str(course)+'_names.dat'

	FRAME_THICKNESS = 3
	FONT_THICKNESS = 2
	MODEL = 'Facenet'

	# Load face encodings
	with open(path_encodings, 'rb') as f:
		known_faces = pickle.load(f)

	# Load face Encodings
	with open(path_names, 'rb') as f:
		known_names = pickle.load(f)

	TOLERANCE = 0.5
	# vid = cv2.VideoCapture(0)
	vid = cv2.VideoCapture(videoPath)
	# Define the codec and create VideoWriter object
	# fourcc = cv2.VideoWriter_fourcc(*'XVID')
	# output = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
	  
	while(True):
	# Now let's loop over a folder of faces we want to label
	# for filename in os.listdir(UNKNOWN_FACES_DIR):
	  # Load image
		ret, frame = vid.read()
		image = frame
	  # image = cv2.imread(f'{UNKNOWN_FACES_DIR}/{filename}')
	  # image = cv2.resize(image,(0,0),None,1,1)

		locations = []
		encodings = []
		face_det = RetinaFace.detect_faces(image)
		match = 0
		for key in face_det.keys():
			identity = face_det[key]
			facial_area = identity["facial_area"]
			x, y, w, h = identity["facial_area"]
	    # cropImg = image[y - 20:h + 20,x - 20:w + 20]
			cropImg = image[y:h,x:w]
			cropImg = cv2.pyrUp(cropImg)
			cropImg = cv2.detailEnhance(cropImg, sigma_s=10, sigma_r=0.15)
			temp = DeepFace.represent(cropImg, model_name=MODEL, model=DeepFace.build_model(MODEL), enforce_detection=False, detector_backend='retinaface', align=True, normalization='base')
			encodings.append(temp)

	    #cv2.rectangle(image, (facial_area[2] + 10, facial_area[3] + 10), (facial_area[0] - 10, facial_area[1] - 10), (255, 255, 255), 2)
	    #cv2.putText(image, str(match), (facial_area[2] - 50, facial_area[3]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (57, 255, 20), FONT_THICKNESS)
			match = match + 1
			locations.append(facial_area)
	  

		for face_encoding, face_location in zip(encodings, locations):
			results = findCosineDistance(known_faces, face_encoding, TOLERANCE)
			match = 'UnKnown'
	    # print(results)
			if True in results:  # If at least one is true, get a name of first of found labels
				match = known_names[results.index(True)]
				markAttendance(match,request)

	    # Get color by name using our fancy function
			color = name_to_color(match)
	    # Each location contains positions in order: top, right, bottom, left
			top_left = (face_location[2], face_location[3])
			bottom_right = (face_location[0], face_location[1])
			cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)
	    # This time we use bottom in both corners - to start from bottom and move 50 pixels down
			top_left = (face_location[2], face_location[3])
			bottom_right = (face_location[0], face_location[1] + 22)
			cv2.putText(image, match, (face_location[0] - 30 , face_location[1] - 10 ), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, FONT_THICKNESS)
	  # Show image
		cv2.imshow("Attendance Box",image)
	  # output.write(image)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	vid.release()
	# output.release()
	# Destroy all the windows
	cv2.destroyAllWindows()


def RegisterAttendance(request):
	teachers_name = request.POST.get('teachers_name')
	subject=request.POST.get('subject')
	course = request.POST.get('course')
	sem = request.POST.get('sem')
	batch_year=request.POST.get('course')

	path_encodings = settings.MEDIA_ROOT+"/Encodings/"+str(course)+".dat"
	path_names = settings.MEDIA_ROOT+"/Encodings/"+str(course)+'_names.dat'

	FRAME_THICKNESS = 3
	FONT_THICKNESS = 2
	MODEL = 'Facenet'

	# Load face encodings
	with open(path_encodings, 'rb') as f:
		known_faces = pickle.load(f)

	# Load face Encodings
	with open(path_names, 'rb') as f:
		known_names = pickle.load(f)

	TOLERANCE = 0.5
	UNKNOWN_FACES_DIR = settings.MEDIA_ROOT+"/Unknown Faces"
	for filename in os.listdir(UNKNOWN_FACES_DIR):
 		# Load image
		image = cv2.imread(f'{UNKNOWN_FACES_DIR}/{filename}')
  	
		locations = []
		encodings = []
		face_det = RetinaFace.detect_faces(image)
		match = 0
		for key in face_det.keys():
			identity = face_det[key]
			facial_area = identity["facial_area"]
			x, y, w, h = identity["facial_area"]
			# cropImg = image[y - 20:h + 20,x - 20:w + 20]
			cropImg = image[y:h,x:w]
			cropImg = cv2.pyrUp(cropImg)
			cropImg = cv2.detailEnhance(cropImg, sigma_s=10, sigma_r=0.15)
			temp = DeepFace.represent(cropImg, model_name=MODEL, model=DeepFace.build_model(MODEL), enforce_detection=False, detector_backend='retinaface', align=True, normalization='base')
			encodings.append(temp)
			match = match + 1
			locations.append(facial_area)
  

		for face_encodings, face_location in zip(encodings, locations):
			results = findCosineDistance(known_faces, face_encodings, TOLERANCE)
			match = 'UnKnown'
    		# print(results)
			if True in results:  # If at least one is true, get a name of first of found labels
				match = known_names[results.index(True)]
				markAttendance(match,request)


from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading

@gzip.gzip_page
def Home(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, 'app1.html')

#to capture video class
class VideoCamera(object):
	def __init__(self):
		self.videoPath = settings.MEDIA_ROOT+"/VideoDemo/output2.avi"
		self.video = cv2.VideoCapture(self.videoPath)
    	# self.video = cv2.VideoCapture(0)
		(self.grabbed, self.frame) = self.video.read()
		threading.Thread(target=self.update, args=()).start()

	def __del__(self):
		self.video.release()

	def get_frame(self):
		image = self.frame
		_, jpeg = cv2.imencode('.jpg', image)
		return jpeg.tobytes()

	def update(self):
		while True:
			(self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


