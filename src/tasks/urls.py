from django.urls import path
from . import views

urlpatterns = [
    path('result_view/', views.ResultView.as_view(), name='ResultView'),
    path("creator/", views.Evaluation.as_view(), name='Evaluation'),
    path("parameter/", views.ParameterUpload.as_view(), name='ParameterUpload'),
    path("sync/", views.EvaluationProcess.as_view(), name='EvaluationProcess'),
    path("condition/", views.InstanceCondition.as_view(), name='InstanceCondition'),
]
