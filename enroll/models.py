from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=70)
    enrollment_no = models.IntegerField()
    file_name = models.FileField(upload_to='')

