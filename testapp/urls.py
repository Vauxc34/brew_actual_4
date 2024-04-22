"""Defines URL patterns for testapp."""
from django.urls import path
from . import views

app_name = 'testapp'
urlpatterns = [
    path('', views.index, name="index"),
    # Page with a list of devices
    path("devices/", views.devices, name="devices"),
    path("values", views.ValueListView.as_view(), name="values"),
    path("variables", views.VariablesListView.as_view(), name="variables"),
    path("variables/<int:pk>/update", views.EditVariableView.as_view(), name="edit_variable"),
    # Page for adding a new device
    path("new_dev/", views.NewDevView.as_view(), name="new_dev"),
    # Page with a single device
    path("devices/<int:dev_id>/", views.device, name="device"),
    # Page for adding a new variable
    path("new_var/", views.NewVariableView.as_view(), name="new_var"),
    # Page for deleting a device
    path("devices/<int:pk>/delete", views.DelDeviceView.as_view(), name="del_dev"),
    # Page for deleting a variable
    path("variables/<int:pk>/delete", views.DelVariableView.as_view(), name="del_var"),

    path("devices/modbus/add", views.ModbusDeviceCreateView.as_view(), name="new_modbus_device")
]
