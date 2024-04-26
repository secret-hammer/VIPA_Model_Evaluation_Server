from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Dataset
from .models import TaskDatasetRelationship
from cv_models.models import Task


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
        public_datasets = Dataset.objects.filter(is_public=True)
        response = []
        for public_dataset in public_datasets:
            response.append({'name': public_dataset.name, 'id': public_dataset.id})
        if request.user.is_authenticated:
            private_datasets = Dataset.objects.filter(user=request.user, is_public=False)
            for private_dataset in private_datasets:
                response.append({'name': private_dataset.name, 'id': private_dataset.id})
        return Response(response)
