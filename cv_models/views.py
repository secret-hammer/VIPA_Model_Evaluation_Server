import zipfile

from django.db.models import Q

from ME.settings import MEDIA_ROOT
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Architecture, TaskArchitectureRelationship, Task, Environment, MetricPerspectiveTaskRelationship, \
    Perspective


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
        relationship = TaskArchitectureRelationship(task=task, architecture=architecture)
        relationship.save()
        return Response({'architecture_id': f'{architecture.id}'}, status=201)


# 上传参数视图


# 查询模型视图
class ArchitectureView(APIView):
    def fillResponse(self, response, architectures):
        for architecture in architectures:
            relationships = TaskArchitectureRelationship.objects.filter(architecture=architecture)
            tasks = []
            for relationship in relationships:
                tasks.append(relationship.task.name)
            response.append({
                'model': architecture.name,
                'id': architecture.id,
                'description': architecture.description,
                'user': architecture.user.username,
                'paper_link': architecture.paper_link,
                'code_link': architecture.code_link,
                'update': architecture.update_time,
                'upload': architecture.upload_time,
                'task': tasks,
            })

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        public_architectures = Architecture.objects.filter(is_public=True)
        response = []
        self.fillResponse(response, public_architectures)
        if request.user.is_authenticated:
            private_architectures = Architecture.objects.filter(user=request.user, is_public=False)
            self.fillResponse(response, private_architectures)
        return Response(response)


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


class MetricView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            task = Task.objects.get(id=request.GET.get("task_id"))
        except:
            return Response({'message': 'wrong task_id'}, status=400)
        task_relationship = MetricPerspectiveTaskRelationship.objects.filter(task=task)
        if not task_relationship:
            return Response({'message': 'Invalid task id'}, status=400)

        default_metrics = {}
        selected_metrics = {}
        for relationship in task_relationship:
            perspective = relationship.perspective
            perspective_name = perspective.name
            perspective_id = perspective.id
            metric_name = relationship.metric.name
            metric_id = relationship.metric.id
            is_default = relationship.is_default
            if is_default:
                if perspective_name not in default_metrics:
                    default_metrics[perspective_name] = {'perspective_name': perspective_name,
                                                         'perspective_id': perspective_id,
                                                         'metrics': [
                                                             {'metric_name': metric_name, 'metric_id': metric_id}]}
                else:
                    default_metrics[perspective_name]['metrics'].append(
                        {'metric_name': metric_name, 'metric_id': metric_id})
            else:
                print(perspective_name)
                if perspective_name not in selected_metrics:
                    selected_metrics[perspective_name] = {'perspective_name': perspective_name,
                                                          'perspective_id': perspective_id,
                                                          'metrics': [
                                                              {'metric_name': metric_name, 'metric_id': metric_id}]}
                else:
                    selected_metrics[perspective_name]['metrics'].append(
                            {'metric_name': metric_name, 'metric_id': metric_id})

        response = {"default_metrics": list(default_metrics.values()),
                    "selected_metrics": list(selected_metrics.values())}
        return Response(response, status=200)


class TaskView(APIView):
    permission_classes = (IsAuthenticated,)

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
