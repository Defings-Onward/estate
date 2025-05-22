from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(unique=True)
    image = models.ImageField(upload_to='dpt_image')
    note = models.TextField()

class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='doctor_image')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    quote = models.CharField()
    facebook_name = models.CharField()
    instagram_name = models.CharField()
    in_name = models.CharField()
    x_name = models.CharField()

class Appointments(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    message = models.TextField()


# Create your models here.
