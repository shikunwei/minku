from django.urls import path
from . import views

app_name = 'cold_call'

urlpatterns = [
    path('', views.cold_call_index, name='cold_call_index'),
    path('spider/', views.cold_call_file_upload, name='cold_call_spider'),
]