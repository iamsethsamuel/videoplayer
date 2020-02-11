from django.db import models

# Create your models here.
class UploadedFiles(models.Model):
    name = models.TextField(max_length=500)
    dateUploaded = models.DateTimeField(auto_now=True) 
    streamType = models.TextField(max_length=10)
    url = models.TextField(max_length=500)
    poster = models.TextField(max_length=500,default='None')
    def __str__(self):
        return "%s %s %s" % (self.name,self.streamType,self.url)
     