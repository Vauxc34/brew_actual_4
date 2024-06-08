from django.shortcuts import render, redirect


from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from .forms import VariableForm, DeviceForm
from .models import Value, Var, Device, ModbusDevice, MyFile

from rest_framework.parsers import MultiPartParser, FormParser

from .models import MyFile, User, ModbusDevice
from .serializers import MyFileSerializer, ModbusDeviceSerializer, UserSerializer 

from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg') 
import pandas as pd
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from io import BytesIO
import base64
from .forms import UploadFileForm
import numpy as np

# Create your views here.

def index(request):
    """The home page for Learning Log."""

    graph = None
    html_table = None
    upload_form = UploadFileForm()
    max_rows = 40
    max_x_axis_rows = 30  # Maximum number of rows for x-axis data
    row_limit_message = None

    if request.method == 'POST' and request.FILES.get('file'):
        upload_form = UploadFileForm(request.POST, request.FILES)
        if upload_form.is_valid():
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)

            try:
                # Read the CSV file
                df = pd.read_csv(fs.path(filename))

                print(pd.__name__)

                # Automatically assign x and y columns based on the first column and subsequent columns
                if df.shape[1] < 2:
                    raise ValueError("CSV file must have at least two columns")

                 

                x_column = df.columns[0]
                y_columns = df.columns[1:]

                # Limit the DataFrame to the first 20 rows
                if len(df) > max_rows:
                    df = df.head(max_rows)
                    row_limit_message = f"The data has been limited to the first {max_rows} rows."

                # Convert DataFrame to HTML
                html_table = df.to_html()

                # Creating the line chart
                plt.figure(figsize=(10, 6))
                for y_column in y_columns:
                    plt.plot(df[x_column], df[y_column], marker='o', linestyle='-', label=y_column)

                if uploaded_file.name == 'Pruszcz_2024_02_14P1correct.csv':
                    plt.xlim(1, 6)
                
                if uploaded_file.name != 'Pruszcz_2024_02_14P1correct.csv':
                    plt.ylim(1, 30)
  
                plt.xlabel(x_column)
                plt.ylabel("Values")
                plt.title(f'Values by {x_column}')
                plt.legend()

                # Saving the plot to a BytesIO object
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()

              

                # Encoding the image in base64 to send to template
                graph = base64.b64encode(image_png).decode('utf-8')

            except Exception as e:
                print("Error processing file:", e)
                return render(request, 'testapp/index.html', {
                    'upload_form': upload_form,
                    'error': 'Error processing file. Please ensure the file has at least two columns.'})


    files = MyFile.objects.all().order_by('id')
    file_serializer = MyFileSerializer(files, many=True)

    datas = User.objects.all().order_by('id')
    data_serializer = UserSerializer(datas, many=True)

    data_dev = ModbusDevice.objects.all()
    data_serializer_dev = ModbusDeviceSerializer(data_dev, many=True)

    context = {
        "files": file_serializer.data, 
        'users': data_serializer.data, 
        'devices': data_serializer_dev.data,
        'graph': graph,
        'upload_form': upload_form,
        'html_table': html_table,
        'row_limit_message': row_limit_message
        }
    return render(request, 'testapp/index.html', context)

def devices(request):
    """Show all devices """
    devices = Device.objects.order_by('date')
    context = {'devices': devices }
    return render(request, 'testapp/devices.html', context)

def device(request, dev_id):
    """show a single device and all its variables"""
    device = Device.objects.get(id = dev_id)
    variables = device.var_set.order_by('user')
    context = {'device': device, 'variables': variables}



    return render(request, 'testapp/dev.html', context)

#def files(request)
  #  return render()

class ValueListView(ListView):
    template_name = "testapp/values.html"
    context_object_name = "values"
    model = Value
    def get_last(self):
        return Question.objects.order_by('date_created')[:5]

class VariablesListView(ListView):
    template_name = "testapp/variables.html"
    context_object_name = "variables"
    model = Var

## new views file added

class MyFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = MyFileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        files = MyFile.objects.all()
        file_serializer = MyFileSerializer(files, many=True)
        return Response(file_serializer.data, status=status.HTTP_200_OK)

    def get(self, request, file_id, *args, **kwargs):
        file_obj = get_object_or_404(MyFile, pk=file_id)
        file_serializer = MyFileSerializer(file_obj)
        return Response(file_serializer.data, status=status.HTTP_200_OK)

class MyFileViewSet(viewsets.ModelViewSet):
 queryset = MyFile.objects.all()
 serializer_class = MyFileSerializer

## new views file added

## new user view

 class MyDataView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        data_serializer = ModbusDeviceSerializer(data=request.data)
        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        datas = ModbusDevice.objects.all()
        data_serializer = ModbusDeviceSerializer(datas, many=True)
        return Response(data_serializer.data, status=status.HTTP_200_OK)

    def get(self, request, data_id, *args, **kwargs):
        data_obj = get_object_or_404(ModbusDevice, pk=data_id)
        data_serializer = ModbusDeviceSerializer(data_obj)
        return Response(data_serializer.data, status=status.HTTP_200_OK)

## new user view

## new user view

class UsersView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        data_serializer = UserSerializer(data=request.data)
        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        datas = User.objects.all()
        data_serializer = UserSerializer(datas, many=True)
        return Response(data_serializer.data, status=status.HTTP_200_OK)

    def get(self, request, data_id, *args, **kwargs):
        data_obj = get_object_or_404(User, pk=data_id)
        data_serializer = UserSerializer(data_obj)
        return Response(data_serializer.data, status=status.HTTP_200_OK)

class UsersViewSet(viewsets.ModelViewSet):
 queryset = User.objects.all()
 serializer_class = UserSerializer

## new user view

## new device view

 class MyDataView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        data_serializer = ModbusDeviceSerializer(data=request.data)
        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        datas = ModbusDevice.objects.all()
        data_serializer = ModbusDeviceSerializer(datas, many=True)
        return Response(data_serializer.data, status=status.HTTP_200_OK)

    def get(self, request, data_id, *args, **kwargs):
        data_obj = get_object_or_404(ModbusDevice, pk=data_id)
        data_serializer = ModbusDeviceSerializer(data_obj)
        return Response(data_serializer.data, status=status.HTTP_200_OK)

class MyDataViewSet(viewsets.ModelViewSet):
 queryset = ModbusDevice.objects.all()
 serializer_class = ModbusDeviceSerializer


## new device view

class EditVariableView(UpdateView):
    template_name = "testapp/update_variable.html"
    success_url = reverse_lazy("testapp:variables")
    form_class = VariableForm
    model = Var

class NewVariableView(CreateView):
    template_name = "testapp/new_variable.html"
    success_url = reverse_lazy("testapp:variables")
    form_class = VariableForm
    model = Var

class NewDevView(CreateView):
    template_name = "testapp/new_dev.html"
    success_url = reverse_lazy("testapp:devices")
    form_class = DeviceForm
    model = Device

class DelDeviceView(DeleteView):
    template_name = "testapp/delete.html"
    success_url = reverse_lazy("testapp:devices")
    form_class = DeviceForm
    model = Device

class DelVariableView(DeleteView):
    template_name = "testapp/delete.html"
    success_url = reverse_lazy("testapp:variables")
    form_class = VariableForm
    model = Var


class ModbusDeviceCreateView(CreateView):
    model = ModbusDevice
    success_url = reverse_lazy("uzupelnic")
    template_name =  "testapp/new_modbus_device.html"
    fields = "__all__"
