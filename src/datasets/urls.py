from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.UploadDataset.as_view(), name='upload-dataset'),
    path('list/', views.ListDataset.as_view(), name='list-dataset'),

]
