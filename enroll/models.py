from django.db import models
#from .views import add_show
# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=70)
    enrollment_no = models.IntegerField()
    file_name = models.FileField(upload_to='')
