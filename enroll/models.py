from django.db import models
import os
import datetime
#from .views import add_show
# Create your models here.


def file_path_dir(instance, file_name):
    return instance.course+'/'+instance.name+'/{1}'.format(instance.id, file_name)

Course_Choice = [('','--Select--'),('MCA','Master In Computer Application'),('MSc','Master In Science')]

Batch_Year = [('','--Select--'),('2019-2020','2019-2020'),('2020-2021','2020-2021'),('2021-2022','2021-2022'),('2022-2023','2022-2023')]

Sem = [('','--Select--'),('1','1'),('2','2'),('3','3'),('4','4')]

Subject = [('','--Select--'),('Artificial Intelligence','Artificial Intelligence'),('Machine Learning','Machine Learning'),('Deep Learning','Deep Learning'),('Reinforcement Learning','Reinforcement Learning'),('Mathematical Foundation','Mathematical Foundation'),('Computer Vision','Computer Vision'),('Numerical Optimization','Numerical Optimization'),('Advanced Python','Advanced Python'),('Natural Language Processing','Natural Language Processing')]


class User(models.Model):
    name = models.CharField(max_length=70)
    course = models.CharField(max_length=10,choices=Course_Choice,default='')
    enrollment_no = models.IntegerField()
    file_name = models.FileField(upload_to=file_path_dir)

class User_attendance_details(models.Model):
    teachers_name = models.CharField(max_length=70)
    student_name = models.CharField(max_length=70,default='')
    enrollment_no = models.IntegerField(default=0)
    subject = models.CharField(max_length=50,choices=Subject,default='')
    course = models.CharField(max_length=10,choices=Course_Choice,default='')
    sem = models.CharField(max_length=10,choices=Sem,default='')
    batch_year = models.CharField(max_length=10,choices=Batch_Year,default='')
    date = models.DateField(("Date"), default=datetime.date.today)
