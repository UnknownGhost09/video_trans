from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.
class User(AbstractUser):
    email=models.EmailField(unique=True)
    verified_at = models.CharField(max_length=200,default='False')
    role =models.CharField(max_length=200,default='user')
    status = models.CharField(max_length=20, default='1')
    updated_at = models.CharField(max_length=200,default=datetime.now())
    created_at = models.CharField(max_length=200,default=datetime.now())
    remember_token=models.CharField(max_length=200,default='False')
    referal_by=models.CharField(max_length=200,null=True)
    referal_code=models.CharField(max_length=200,unique=True,default='0000')
    phone_no=models.CharField(max_length=200,null=True)
    activation_date=models.CharField(max_length=200,default='N/A')


    class Meta:
        db_table='users'



class Video(models.Model):
    
    videofile= models.FileField(upload_to='', null=True, verbose_name="")

    def __str__(self):
        return self.name + ": " + str(self.videofile)
    class Meta:
        db_table='video'


class ConvertedVideo(models.Model):
    video_id=models.ForeignKey("core.Video", db_column='video_id', on_delete=models.CASCADE)
    videofile= models.FileField(upload_to='', null=True, verbose_name="")
    type=models.CharField(max_length=200)

    def __str__(self):
        return self.name + ": " + str(self.videofile)
    class Meta:
        db_table='convertedvideo'

class Transcript(models.Model):
    video_id=models.ForeignKey("core.Video", db_column='video_id', on_delete=models.CASCADE)
    c_id=models.ForeignKey("core.ConvertedVideo", db_column='c_id', on_delete=models.CASCADE)
    script=models.TextField(null=True)
    
    class Meta:
        db_table='transcript'