from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone




def get_default_my_date():
  return datetime.datetime.now() + datetime.timedelta(days=7)

class File(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField( max_length=200)
    content=models.TextField(max_length=200)
    date_posted=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)
    date_expired=models.DateTimeField(default=get_default_my_date)
    
    commentPermit=models.ManyToManyField(User,related_name='commentpermit')
    showPermit=models.ManyToManyField(User,related_name='showpermit')
    file=models.FileField(upload_to='files', max_length=100)

    def __str__(self):
        return self.title
    
    def __repr__(self):
        return f"File('{self.showPermit}','{self.commentPermit}')"


class Comment(models.Model):
    post=models.ForeignKey(File, on_delete=models.CASCADE,related_name ='post')
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    date_comment=models.DateTimeField(auto_now_add=True)
    date_edited=models.DateTimeField(auto_now=True)
    content=models.TextField()
    


class ip(models.Model):
    username=models.CharField(default="no",max_length=50)
    pub_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    os=models.CharField(default="no",max_length=1000)
    
    
    def __str__(self):
        return self.username
    

