from django.db import models
import os

from django.db.models.enums import Choices
#from .views import add_show
# Create your models here.


def file_path_dir(instance, file_name):
    return instance.course+'/'+instance.semester+'/'+instance.name+'/{1}'.format(instance.id, file_name)

Course_Choice = [('','--Select--'),('MCA','MCA'),('MSc','M.Sc')]
Sem_Choice = [('','--Select--'),('1','1'),('2','2'),('3','3'),('4','4')]

class User(models.Model):
    name = models.CharField(max_length=70)
    course = models.CharField(max_length=10,choices=Course_Choice,default='')
    semester = models.CharField(max_length=2,choices=Sem_Choice,default='')
    enrollment_no = models.IntegerField()
    file_name = models.FileField(upload_to=file_path_dir)
