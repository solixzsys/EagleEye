
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
    channel_id=models.CharField(max_length=200,primary_key=True,default=str(datetime.datetime.now()))
    channel_name=models.CharField(max_length=200)
    country_id=models.CharField(max_length=200)

    def __str__(self):
        return self.country_code

