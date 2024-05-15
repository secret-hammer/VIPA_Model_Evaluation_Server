import zipfile

from django.db.models import Q

from ME.settings import MEDIA_ROOT
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Architecture, Task, Environment, Perspective, Parameter, Metric


# 上传模型视图

class upload_architecture(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        zip_file = request.FILES.get('file')
        if not zip_file:
            return Response({'error': 'No file uploaded'}, status=400)
        name = request.POST.get('name')
        description = request.POST.get('description')
        paper_link = request.POST.get('paper_link')
        code_link = request.POST.get('code_link')
        is_public = request.POST.get('is_public')
        architecture = Architecture(user=request.user, name=name, description=description, paper_link=paper_link,
                                    code_link=code_link, is_public=is_public)

        task_id = request.POST.get('task_id')
        try:
            task = Task.objects.get(id=task_id)
            architecture.task = task
        except:
            return Response({'message': 'Invalid task id'}, status=400)
        
        
        try:
            with zipfile.ZipFile(zip_file, 'r') as zipobj:
                for file_info in zipobj.infolist():
                    file_name = file_info.filename.split('/')[-1]
                    if file_name == 'model.py':
                        break
                else:
                    return Response({'message': f'{zipobj.namelist()}'}, status=400)
        except:
            return Response({'message': 'zip_file needed'}, status=400)
        architecture.save()
        architecture.file = zip_file
        architecture.save()
        architecture.file_save()
        return Response({'architecture_id': f'{architecture.id}'}, status=201)


# 查询模型视图
class ArchitectureView(APIView):
    def get(self, request):
        task_id = request.GET.get('task_id')
        
        architectures = Architecture.objects.filter(Q(user=request.user) | Q(is_public=True)) if request.user.is_authenticated else Dataset.objects.filter(is_public=True)
        
        if task_id is not None:
            architectures = architectures.filter(task_id=task_id)
            
        return Response([arch.to_dict() for arch in architectures.distinct()])


class ArchitectureCheck(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            architecture = Architecture.objects.get(
                (Q(is_public=True) | Q(user=request.user)) & Q(id=request.GET.get("architecture_id")))
        except:
            return Response({'message': 'Invalid architecture id'}, status=400)
        response = {"model_name": architecture.name, "description": architecture.description}
        return Response(response, status=200)

# 查询模型权重
class ParameterView(APIView):
    def get(self, request):
        architecture_id = request.GET.get('architecture_id')
        
        parameters = Parameter.objects.filter(Q(user=request.user) | Q(is_public=True)) if request.user.is_authenticated else Parameter.objects.filter(is_public=True)
        
        if architecture_id is not None:
            parameters = parameters.filter(architecture_id=architecture_id)
            
        return Response([para.to_dict() for para in parameters.distinct()])
        
        
# 查询可用评估指标
class MetricView(APIView):
    def get(self, request):
        task_id = request.GET.get('task_id')
        aspect_id = request.GET.get('aspect_id')
        perspective_id = request.GET.get('perspective_id')
        
        metrics = Metric.objects.all()
        
        if task_id is not None:
            metrics = metrics.filter(task_id=task_id)
        
        if aspect_id is not None:
            metrics = metrics.filter(aspect_id=aspect_id)
            
        if perspective_id is not None:
            metrics = metrics.filter(perspective_id=perspective_id)
            
        return Response([metric.to_dict() for metric in metrics])


class TaskView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        response = []
        for task in tasks:
            response.append({'id': task.id, 'name': task.name})
        return Response(response)


class EnvironmentList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        environments = Environment.objects.all()
        response = []
        for environment in environments:
            response.append({'id': environment.id, 'name': environment.name})
        return Response(response)
