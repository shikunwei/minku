from django.urls import path
from . import views

app_name = 'cold_call'

urlpatterns = [
    path('', views.cold_call_index, name='cold_call_index'),
    path('<int:cold_call_id>/', views.cold_call_detail, name='cold_call_detail'),
    path('spider/', views.cold_call_file_upload, name='cold_call_spider'),
    path('add_cold_call_comment/<int:cold_call_id>', views.add_cold_call_comment, name='add_cold_call_comment'),
]