from django.forms import ModelForm
from django import forms
from .models import Var, Device


class VariableForm(ModelForm):
    class Meta:
        model = Var
        exclude = ["date", "date_updated"]

class DeviceForm(ModelForm):
    class Meta:
        model = Device
        exclude = ["date"]

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a file') 