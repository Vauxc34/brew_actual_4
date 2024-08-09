from django.forms import ModelForm
from django import forms
from .models import Var, Device, Event

class UploadFileForm(forms.Form):
    file = forms.FileField()

class VariableForm(ModelForm):
    class Meta:
        model = Var
        exclude = ["date", "date_updated"]

class DeviceForm(ModelForm):
    class Meta:
        model = Device
        exclude = ["date"]

class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ["sms"]

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a file') 