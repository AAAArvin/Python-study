from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('check/', delete_datum, name='check'),
    path('<int:data_pk>/', detail, name='detail'),
    path('download/', download_data_csv, name='download'),
    path('file/', file_manage, name='file'),
    path('upload/', index, name='upload'),
    path('<str:file_time>/<int:file_pk>', import_data_from_files, name='import_data_from_files'),
]

