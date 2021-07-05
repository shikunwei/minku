from django.urls import path
from . import views

app_name = 'candidates'

urlpatterns = [
    path('', views.candidates_index, name='candidates_index'),
    path('<int:candidate_id>/', views.candidate_detail, name='candidate_detail'),
    path('spider/', views.candidate_file_upload, name='candidates_spider'),
    path('add_candidate_comment/<int:candidate_id>', views.add_candidate_comment, name='add_candidate_comment'),
]