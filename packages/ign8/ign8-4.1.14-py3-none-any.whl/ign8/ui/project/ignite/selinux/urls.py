
from django.urls import path, include
from .views import selinux_list, selinux_event_list , UploadSelinuxDataView, UploadSElinuxEventView
from .views import SetroubleshootEntry_list, SetroubleshootEntry_host, SetroubleshootEntryAPIview
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('', selinux_list, name='selinux_list'),
    path('selinux_list/', selinux_list, name='selinux_list'),
    path('selinux_event_list/', selinux_event_list, name='selinux_event_list'),
    path('upload_selinux_data/', UploadSelinuxDataView.as_view(), name='upload_selinux_data'),
    path('upload_selinux_event/', UploadSElinuxEventView.as_view(), name='upload_selinux_event'),
    path('api/setroubleshoot/upload/', SetroubleshootEntryAPIview.as_view(), name='upload_setroubleshoot_entry'),
    path('SetroubleshootEntry/<str:hostname>/', SetroubleshootEntry_host, name='SetroubleshootEntry_host'),
    path('SetroubleshootEntry_list/', SetroubleshootEntry_list, name='SetroubleshootEntry_list'),
    path('SetroubleshootEntry_list_full/', SetroubleshootEntry_list, name='SetroubleshootEntry_list'),
]

