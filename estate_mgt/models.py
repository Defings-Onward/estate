from django.db import models
from django.contrib.auth.models import User


class Properties(models.Model):
    details = models.TextField()
    type = models.CharField(max_length=30)
    location = models.CharField(max_length=1000)
    status = models.CharField(max_length=30)
    area = models.CharField(max_length=30)
    beds = models.IntegerField()
    baths = models.IntegerField()
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    price = models.TextField()
    image = models.ImageField(upload_to='ppt_image', blank=True, null=True) 
    video = models.ImageField(upload_to='ppt_video', blank=True, null=True)
    address = models.TextField(null=True)
    visible = models.BooleanField(default=False)
    taken = models.BooleanField(default=False)

class visits(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

class services(models.Model):
    bi = models.TextField()
    head = models.TextField()
    body = models.TextField()
    image = models.TextField()
    name = models.TextField()
    dis_body = models.TextField(default="A Header")

class Notification(models.Model):
    body = models.TextField()
    head = models.TextField(null=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)

class Application(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    cleared = models.BooleanField(default=False)
# Create your models here.
