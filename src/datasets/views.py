from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Dataset
from .models import TaskDatasetRelationship
from cv_models.models import Task
from django.db.models import Q
from django.core import serializers


# Create your views here.
class UploadDataset(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=400)
        name = request.POST.get('name')
        description = request.POST.get('description')
        paper_link = request.POST.get('paper_link')
        is_public = request.POST.get('is_public')
        task_id = request.POST.get('task_id')
        try:
            task = Task.objects.get(id=task_id)
        except:
            return Response({'message': 'Invalid task id'}, status=400)
        dataset = Dataset(user=request.user, name=name, description=description, paper_link=paper_link,
                          is_public=is_public)
        dataset.save()
        dataset.file = file
        dataset.save()
        relationship = TaskDatasetRelationship(task=task, dataset=dataset)
        relationship.save()
        return Response({'message': f'File{dataset.id} uploaded successfully'},status=201)


class ListDataset(APIView):
    def get(self, request):
        
        # 参数提取
        task_id = request.GET.get('task_id')

       # 基础的 QuerySet，如果用户已认证，包括用户的私有数据集和公开的数据集，如果用户未认证，只包括公开的数据集
        datasets = Dataset.objects.filter(Q(user=request.user) | Q(is_public=True)) if request.user.is_authenticated else Dataset.objects.filter(is_public=True)

        if task_id is not None:
            # 根据task_id寻找所有可用的数据集id
            task_related_dataset_ids = TaskDatasetRelationship.objects.filter(task_id=task_id).values_list('dataset_id', flat=True)
            
            # 添加额外的过滤条件
            datasets = datasets.filter(id__in=task_related_dataset_ids)

        # 去重
        datasets = datasets.distinct()
        
        # 加入该数据集的可用任务id
        for dataset in datasets:
            task_ids = TaskDatasetRelationship.objects.filter(dataset_id=dataset.id).values_list('task_id', flat=True)
            dataset.task_ids = list(task_ids)
                
        return Response([dataset.to_dict() for dataset in datasets])
