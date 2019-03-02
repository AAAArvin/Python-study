from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('check/', delete_datum, name='check'),
    path('<int:data_pk>/', detail, name='detail'),
    path('download/', download_data_csv, name='download'),
]