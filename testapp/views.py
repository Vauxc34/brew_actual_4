from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from .forms import VariableForm, DeviceForm, EventForm
from .models import Value, Var, Device, ModbusDevice, MyFile

from rest_framework.parsers import MultiPartParser, FormParser

from .models import MyFile, User, ModbusDevice, Event
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
from django.conf import settings
from io import BytesIO
import os
import base64
from .forms import UploadFileForm
from .models import UploadedFile
import numpy as np

# Create your views here.

def handle_uploaded_file(f, folder=''):
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    
    # Save the uploaded file
    file_path = os.path.join(settings.MEDIA_ROOT, f.name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    # Check if the file already exists in the database
    uploaded_file, created = UploadedFile.objects.get_or_create(
        file=f.name,
        defaults={'file_path': file_path}
    )
    
    # If the file was not created (i.e., it already exists), update the path
    if not created:
        uploaded_file.file_path = file_path
        uploaded_file.save()
    
    return file_path

def index(request):
    """The home page for Learning Log."""

    graph = None
    html_table = None
    upload_form = UploadFileForm()
    special_upload_form = UploadFileForm()  # New form for special upload
    max_rows = 40
    max_x_axis_rows = 30
    row_limit_message = None
    column_options = None
    error = None

    # Fetch all uploaded files from the database
    files = UploadedFile.objects.all()

        # Synchronize the database with the files in the media directory
    media_files = os.listdir(settings.MEDIA_ROOT)
    db_files = set(UploadedFile.objects.values_list('file', flat=True))

    # Add files that are in the media directory but not in the database
    for file_name in media_files:
        if file_name not in db_files:
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            UploadedFile.objects.create(file=file_name, file_path=file_path)

    # Remove database entries for files that no longer exist in the media directory
    for db_file in db_files:
        if db_file not in media_files:
            UploadedFile.objects.filter(file=db_file).delete()

    # Check if files exist in the specified folder and remove from the database if they don't
    for file in files:
        if not os.path.exists(file.file_path):
            file.delete()

    if request.method == 'POST':
        if 'file' in request.FILES:
            upload_form = UploadFileForm(request.POST, request.FILES)
            if upload_form.is_valid():
                uploaded_file = request.FILES['file']
                file_path = handle_uploaded_file(uploaded_file)
                
                # Save the uploaded file information to the database
                UploadedFile.objects.create(file=uploaded_file.name, file_path=file_path)
                
                try:
                    df = pd.read_csv(file_path)

                    # Ensure the CSV file has at least two columns
                    if df.shape[1] < 2:
                        raise ValueError("CSV file must have at least two columns")

                    x_column = df.columns[0]
                    y_columns = df.columns[1:]

                    # Ensure only numeric columns are processed
                    numeric_y_columns = df[y_columns].select_dtypes(include=['number']).columns

                    if len(numeric_y_columns) == 0:
                        raise ValueError("CSV file must have at least one numeric column")

                    # Normalize numeric y_columns to a 0-1 range
                    df[numeric_y_columns] = (df[numeric_y_columns] - df[numeric_y_columns].min()) / (df[numeric_y_columns].max() - df[numeric_y_columns].min())

                    # Invert the normalized values
                    df[numeric_y_columns] = 1 - df[numeric_y_columns]

                    # Extract the date portion from the datetime string
                    df['Date'] = pd.to_datetime(df[x_column], errors='coerce').dt.date
                    if df['Date'].isnull().all():
                        raise ValueError("The first column must contain valid datetime values")

                    # Preserve the original row order
                    df['OriginalIndex'] = df.index

                    # Aggregate numeric y-columns by date
                    df_aggregated = df.groupby('Date')[numeric_y_columns].mean().reset_index()

                    # Restore the original row order based on the first appearance of each date
                    first_indices = df.groupby('Date')['OriginalIndex'].min().reset_index()
                    df_aggregated = pd.merge(df_aggregated, first_indices, on='Date').sort_values(by='OriginalIndex').drop(columns=['OriginalIndex'])

                    # Normalize numeric y_columns to a 0-1 range
                    df_aggregated[numeric_y_columns] = (df_aggregated[numeric_y_columns] - df_aggregated[numeric_y_columns].min()) / (df_aggregated[numeric_y_columns].max() - df_aggregated[numeric_y_columns].min())

                    # Convert the DataFrame to HTML
                    html_table = df.to_html()

                    # Create the bar plot
                    plt.figure(figsize=(10, 6))
                    bar_width = 0.35  # Adjust the width of the bars

                    num_bars = len(numeric_y_columns)
                    index = np.arange(len(df_aggregated))

                    for i, y_column in enumerate(numeric_y_columns):
                        plt.bar(index + i * bar_width, df_aggregated[y_column], width=bar_width, label=y_column)

                    # Adjust the x-axis ticks based on max_x_axis_rows
                    if len(df_aggregated) > max_x_axis_rows:
                        plt.xticks(ticks=np.arange(0, len(df_aggregated), len(df_aggregated) // max_x_axis_rows),
                                   labels=df_aggregated['Date'].iloc[::len(df_aggregated) // max_x_axis_rows], rotation=45)
                    else:
                        plt.xticks(ticks=index + bar_width * (num_bars / 2), labels=df_aggregated['Date'], rotation=45)

                    plt.xlabel(x_column)
                    plt.ylabel("Inverted Normalized Values")
                    plt.title(f'Inverted Normalized Values by {x_column}')
                    plt.legend()
                    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)  # Adjust these values as needed

                    # Save the plot to a BytesIO buffer
                    buffer = BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    image_png = buffer.getvalue()
                    buffer.close()

                    # Encode the image in base64 to send to the template
                    graph = base64.b64encode(image_png).decode('utf-8')

                    # Store the DataFrame in the session
                    request.session['df'] = df.to_json()
                    column_options = list(df_aggregated['Date'])

                except Exception as e:
                    print("Error processing file:", e)
                    error = 'Error processing file. Please ensure the file has at least two columns, one of which is numeric.'
        elif 'selected_date' in request.POST:
            selected_date = request.POST.get('selected_date')
            df = pd.read_json(request.session['df'])
            df['Date'] = pd.to_datetime(df[df.columns[0]], errors='coerce').dt.date

            # Filter the DataFrame for the selected date
            df_filtered = df[df['Date'] == pd.to_datetime(selected_date).date()]

            if df_filtered.empty:
                graph = None
                error = f"No data available for the selected date: {selected_date}"
            else:
                # Create a new line plot for the filtered data
                plt.figure(figsize=(10, 9))

                # Determine the index of the selected date
                selected_index = df_filtered.index[0]

                # Define the range of indices to plot (include two records before and after the selected date)
                start_index = max(selected_index - 2, 0)
                end_index = min(selected_index + 3, len(df))

                for column in df_filtered.columns[1:]:
                    if column != 'Date' and df_filtered[column].dtype in [np.float64, np.int64]:
                        plt.plot(df.index[start_index:end_index], df[column].iloc[start_index:end_index], marker='o', label=column)

                plt.xlabel('Index')
                plt.ylabel('Values')
                plt.title(f'Values around {selected_date}')
                plt.legend()
                plt.xticks(df.index[start_index:end_index], df['Date'].iloc[start_index:end_index], rotation=45)                

                # Save the plot to a BytesIO buffer
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()

                # Encode the image in base64 to send to the template
                graph = base64.b64encode(image_png).decode('utf-8')
        elif 'selected_file' in request.POST:  # Handling the 'Check the chart' button
            selected_file_id = request.POST.get('selected_file')
            if selected_file_id:
                selected_file = UploadedFile.objects.get(id=selected_file_id)
                file_path = selected_file.file_path

                try:
                    df = pd.read_csv(file_path)

                    # Ensure the CSV file has at least two columns
                    if df.shape[1] < 2:
                        raise ValueError("CSV file must have at least two columns")

                    x_column = df.columns[0]
                    y_columns = df.columns[1:]

                    # Ensure only numeric columns are processed
                    numeric_y_columns = df[y_columns].select_dtypes(include=['number']).columns

                    if len(numeric_y_columns) == 0:
                        raise ValueError("CSV file must have at least one numeric column")

                    # Normalize numeric y_columns to a 0-1 range
                    df[numeric_y_columns] = (df[numeric_y_columns] - df[numeric_y_columns].min()) / (df[numeric_y_columns].max() - df[numeric_y_columns].min())

                    # Invert the normalized values
                    df[numeric_y_columns] = 1 - df[numeric_y_columns]

                    # Extract the date portion from the datetime string
                    df['Date'] = pd.to_datetime(df[x_column], errors='coerce').dt.date
                    if df['Date'].isnull().all():
                        raise ValueError("The first column must contain valid datetime values")

                    # Preserve the original row order
                    df['OriginalIndex'] = df.index

                    # Aggregate numeric y-columns by date
                    df_aggregated = df.groupby('Date')[numeric_y_columns].mean().reset_index()

                    # Restore the original row order based on the first appearance of each date
                    first_indices = df.groupby('Date')['OriginalIndex'].min().reset_index()
                    df_aggregated = pd.merge(df_aggregated, first_indices, on='Date').sort_values(by='OriginalIndex').drop(columns=['OriginalIndex'])

                    # Normalize numeric y_columns to a 0-1 range
                    df_aggregated[numeric_y_columns] = (df_aggregated[numeric_y_columns] - df_aggregated[numeric_y_columns].min()) / (df_aggregated[numeric_y_columns].max() - df_aggregated[numeric_y_columns].min())

                    # Convert the DataFrame to HTML
                    html_table = df.to_html()

                    # Create the bar plot
                    plt.figure(figsize=(10, 6))
                    bar_width = 0.35  # Adjust the width of the bars

                    num_bars = len(numeric_y_columns)
                    index = np.arange(len(df_aggregated))

                    for i, y_column in enumerate(numeric_y_columns):
                        plt.bar(index + i * bar_width, df_aggregated[y_column], width=bar_width, label=y_column)

                    # Adjust the x-axis ticks based on max_x_axis_rows
                    if len(df_aggregated) > max_x_axis_rows:
                        plt.xticks(ticks=np.arange(0, len(df_aggregated), len(df_aggregated) // max_x_axis_rows),
                                   labels=df_aggregated['Date'].iloc[::len(df_aggregated) // max_x_axis_rows], rotation=45)
                    else:
                        plt.xticks(ticks=index + bar_width * (num_bars / 2), labels=df_aggregated['Date'], rotation=45)

                    plt.xlabel(x_column)
                    plt.ylabel("Inverted Normalized Values")
                    plt.title(f'Inverted Normalized Values by {x_column}')
                    plt.legend()
                    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)  # Adjust these values as needed

                    # Save the plot to a BytesIO buffer
                    buffer = BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    image_png = buffer.getvalue()
                    buffer.close()

                    # Encode the image in base64 to send to the template
                    graph = base64.b64encode(image_png).decode('utf-8')

                    # Store the DataFrame in the session
                    request.session['df'] = df.to_json()
                    column_options = list(df_aggregated['Date'])

                except Exception as e:
                    print("Error processing file:", e)
                    error = 'Error processing file. Please ensure the file has at least two columns, one of which is numeric.'


    files = UploadedFile.objects.all().order_by('id')
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
        'row_limit_message': row_limit_message,
        'max_rows': max_rows,
        'max_x_axis_rows': max_x_axis_rows,
        'column_options': column_options,
        'special_upload_form': special_upload_form,
        'files': UploadedFile.objects.all(),  # Refresh the files list after deletion,
        'error': error
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

def events(request):
    """Show all events """
    events = Event.objects.order_by('name')
    context = {'events': events }
    return render(request, 'testapp/events.html', context)

def event(request, event_id):
    """show a single event and all its variables"""
    event = Event.objects.get(id = event_id)
    context = { 'event': event }
    return render(request, 'testapp/event.html', context)

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

class NewEventView(CreateView):
    template_name = "testapp/new_event.html"
    success_url = reverse_lazy("testapp:events")
    form_class = EventForm
    model = Event

class DelEventView(DeleteView):
    template_name = "testapp/delete.html"
    success_url = reverse_lazy("testapp:events")
    form_class = EventForm
    model = Event

class UpdateEventView(UpdateView):
    template_name = "testapp/update_event.html"
    success_url = reverse_lazy("testapp:events")
    form_class = EventForm
    model = Event

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