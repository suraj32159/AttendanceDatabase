from django.db import models
import os
#from .views import add_show
# Create your models here.


def file_path_dir(instance, file_name):
    return instance.name+'/{1}'.format(instance.id, file_name)

class User(models.Model):
    name = models.CharField(max_length=70)
    enrollment_no = models.IntegerField()
    file_name = models.FileField(upload_to=file_path_dir)
