from rest_framework import serializers
from .models import MyFile, ModbusDevice, User

class MyFileSerializer(serializers.ModelSerializer):
 class Meta:
    model = MyFile
    fields = ('file', 'description', 'uploaded_at')

class ModbusDeviceSerializer(serializers.ModelSerializer):
  class Meta:
    model = ModbusDevice
    fields = ('name', 'ip', 'reg_first', 'reg_amount', 'date_updated', 'frequency', 'enabled', 'user')

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('email', 'password', 'first_name')