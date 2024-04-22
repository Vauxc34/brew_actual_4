from django.forms import ModelForm

from .models import Var, Device


class VariableForm(ModelForm):
    class Meta:
        model = Var
        exclude = ["date", "date_updated"]

class DeviceForm(ModelForm):
    class Meta:
        model = Device
        exclude = ["date"]
