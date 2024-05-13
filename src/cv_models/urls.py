from django.urls import path
from . import views

urlpatterns = [
    path('upload/architecture/', views.upload_architecture.as_view(), name='upload_architecture'),
    path('list/architecture/', views.ArchitectureView.as_view(), name='ArchitectureView'),
    path('check/architecture/', views.ArchitectureCheck.as_view(), name='ArchitectureCheck'),
    path('list/metrics/', views.MetricView.as_view(), name='MetricView'),
    path('task_view/', views.TaskView.as_view(), name='TaskView'),
    path('environments/', views.EnvironmentList.as_view(), name='EnvironmentList'),
    path('list/parameters/', views.ParameterView.as_view(), name='ParameterView')
]
