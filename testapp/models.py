from django.db import models
from datetime import datetime

# Create your models here.


## new file model

class MyFile(models.Model):
 file = models.FileField(blank=False, null=False,upload_to='docs/')
 description = models.CharField(null=True,max_length=255)
 uploaded_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return self.description

## new file model


class AlembicVersion(models.Model):
    version_num = models.CharField(primary_key=True, max_length=255)
 
class Note(models.Model):
    note = models.CharField(blank=True, null=True, max_length=255)
    sec = models.IntegerField(blank=True, null=True)
    data = models.CharField(blank=True, null=True, max_length=255)
    date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)



class User(models.Model):
    email = models.CharField(blank=True, null=True, max_length=255)
    password = models.CharField(blank=True, null=True, max_length=255)
    first_name = models.CharField(blank=True, null=True, max_length=255)


    def __str__(self):
        return f"{self.first_name} ({self.email})"

class ModbusDevice(models.Model):
    name = models.CharField(max_length=100)
    ip = models.CharField(max_length=20)
    reg_first = models.IntegerField(blank=True, null=True)
    reg_amount = models.IntegerField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    frequency = models.IntegerField(blank=True, null=True)
    enabled = models.BooleanField(blank=True, null=True)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="modbus_devices")

class ModbusDeviceValue(models.Model):
    device = models.ForeignKey(to=ModbusDevice, on_delete=models.PROTECT, related_name="values")
    date_updated = models.DateTimeField(auto_now=True)
    value = models.TextField()

