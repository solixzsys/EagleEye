
from django.db import models
import datetime

class Country(models.Model):
    country_code=models.CharField(max_length=200,primary_key=True,default=str(datetime.datetime.now()))
    country_name=models.CharField(max_length=200)
    continent=models.CharField(max_length=200)

    def __str__(self):
        return self.country_code

    def save(self,*args,**kwargs):
        self.country_code=str(self.country_name).replace(" ","_")
        super(Country,self).save(*args,**kwargs)

class Channel(models.Model):
    
    channel_name=models.CharField(max_length=200,primary_key=True)
    channel_url=models.URLField()
    country_id=models.ForeignKey(Country)

    def __str__(self):
        return self.channel_name

class Entry(models.Model):
    
    heading=models.CharField(max_length=200,primary_key=True)
    #summary=models.URLField()
    page=models.URLField()
    thumbnail=models.URLField()
    date=models.DateField()
    channel=models.ForeignKey(Channel)

    def __str__(self):
        return self.heading

class Story(models.Model):
    #id=models.AutoField()
    heading = models.ForeignKey(Entry)
    content=models.TextField()
    
    def __str__(self):
        return self.heading.heading
    

    