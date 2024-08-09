"""Defines URL patterns for testapp."""
from django.urls import path
from . import views

#MyFileViewSet, MyDataViewSet, UsersViewSet

app_name = 'testapp'
urlpatterns = [
    path('', views.index, name="index"),
    # Page with a list of devices
    path("devices/", views.devices, name="devices"),
    path("events/", views.events, name="events"),
    path("values", views.ValueListView.as_view(), name="values"),
    path("variables", views.VariablesListView.as_view(), name="variables"),
    path("variables/<int:pk>/update", views.EditVariableView.as_view(), name="edit_variable"),
    path("events/<int:pk>/update", views.UpdateEventView.as_view(), name="update_event"),
    # Page for adding a new device
    path("new_dev/", views.NewDevView.as_view(), name="new_dev"),
    # Page with a single device
    path("devices/<int:dev_id>/", views.device, name="device"),
    path("events/<int:event_id>/", views.event, name="event"),
    # Page for adding a new variable
    path("new_var/", views.NewVariableView.as_view(), name="new_var"),
    path("new_event/", views.NewEventView.as_view(), name="new_event"),
    # Page for deleting a device
    path("devices/<int:pk>/delete", views.DelDeviceView.as_view(), name="del_dev"),
    path("variables/<int:pk>/delete", views.DelVariableView.as_view(), name="del_var"),
    path("events/<int:pk>/delete", views.DelEventView.as_view(), name="del_event"),
    path("devices/modbus/add", views.ModbusDeviceCreateView.as_view(), name="new_modbus_device"),
]
