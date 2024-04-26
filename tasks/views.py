import json

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ME.settings import EVALUATE_IP_PORT, MEDIA_ROOT
from datasets.models import Dataset
from .models import Metric, ModelInstance, InstanceMetricPerspectiveRelationship, Parameter
from cv_models.models import Architecture, Task, Environment, Perspective, Aspect
import requests
import os


# Create your views here.


class ResultView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        dataset_id = request.data.get('dataset_id')
        task_id = request.data.get('task_id')
        aspects_ids = request.data.get('aspects_ids')
        try:
            instances = ModelInstance.objects.filter(user=user)
            if task_id:
                instances = instances.objects.filter(task_id=task_id)
            if dataset_id:
                instances = instances.objects.filter(dataset_id=dataset_id)
        except:
            return Response({'message': f"{dataset_id, task_id}No instance find"}, status=400)
        response = []

        for instance in instances:
            if aspects_ids and aspects_ids != []:
                instances = instances.objects.filter(aspect__id__in=aspects_ids)

            # return Response({f'{instances}'})
            evaluate_score = {}
            if instance.condition == 2:
                relationships = InstanceMetricPerspectiveRelationship.objects.filter(instance=instance)
                for relationship in relationships:
                    metric = relationship.metric
                    score = relationship.score
                    scores = {'metric_name': metric.name, 'metric_score': score}
                    perspective = relationship.perspective
                    perspective_name = perspective.name
                    if perspective_name not in evaluate_score:
                        evaluate_score[perspective_name] = {'perspective_name': perspective_name,
                                                            'metric_names': [scores]}
                    else:
                        evaluate_score[perspective_name]['metric_names'].append(scores)
                response.append({'model_architecture_name': instance.architecture.name,
                                 'evaluate_score': list(evaluate_score.values()),
                                 'parameter_size': 1,
                                 'user_name': instance.user.username,
                                 'paper_link': instance.architecture.paper_link,
                                 'code_link': instance.architecture.code_link,
                                 'model_instance_id': instance.id})
        return Response(response, status=200)


class Evaluation(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        environment_id = request.data.get('environment_id')
        architecture_id = request.data.get('model_arch_id')
        task_id = request.data.get('task_id')
        dataset_id = request.data.get('dataset_id')
        perspectives_metrics = request.data.get('perspectives_metrics')
        aspect_id = request.data.get('aspect_id')
        parameter_id = request.data.get('parameter_id')
        try:
            architecture = Architecture.objects.get(id=architecture_id)
            task = Task.objects.get(id=task_id)
            dataset = Dataset.objects.get(id=dataset_id)
            environment = Environment.objects.get(id=environment_id)
            aspect = Aspect.objects.get(id=aspect_id)
            parameter = Parameter.objects.get(id=parameter_id)
        except:
            return Response({
                'message': f'Invalid arch{architecture_id}/task{task_id}/dataset{dataset_id}/environment{environment_id}/aspect{aspect_id}/parameter id{parameter_id}'},
                status=400)
        instance = ModelInstance(user=request.user, architecture=architecture, task=task, dataset=dataset,
                                 environment=environment, aspect=aspect, parameter=parameter)
        instance.save()
        name_perspectives_metrics = []
        for perspective_metric in perspectives_metrics:
            try:
                perspective = Perspective.objects.get(id=perspective_metric['perspective_id'])
            except:
                return Response({'message': f'{perspective_metric}perspective_metric'}, status=400)
            name_perspective_metric = {'perspective_name': perspective.name, 'metrics': []}
            for metric_id in perspective_metric['metrics_ids']:
                try:
                    metric = Metric.objects.get(id=metric_id)
                except:
                    return Response({'message': f'{metric_id}metric_id'}, status=400)
                relationship = InstanceMetricPerspectiveRelationship(instance=instance, metric=metric,
                                                                     perspective=perspective)
                relationship.save()
                name_perspective_metric['metrics'].append({'metric_name': metric.name, 'metric_score': 0})
            name_perspectives_metrics.append(name_perspective_metric)
            model_path = instance.architecture.model_path
            dataset_path = instance.dataset.file.name
            dataset_principal = instance.dataset.principal
            parameter_path = instance.parameter.file.name
            message = {'task_name': instance.task.name, 'perspective_metric': name_perspectives_metrics,
                       'model_path': model_path,
                       'parameter': parameter_path,
                       'dataset_path': dataset_path,
                       'dataset_principal': dataset_principal,
                       'instance_id': instance.id}
        response = requests.post(url="http://127.0.0.1:3308/start/", json=message)
        if response.status_code == 200:
            return Response({'instance_id': instance.id}, status=200)
        else:
            return Response({'message': f'Evaluation fail to start{parameter_path}'}, status=400)


class EvaluationProcess(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        instance_id = int(request.data['instance_id'])
        condition = int(request.data['condition'])
        try:
            instance = ModelInstance.objects.get(id=instance_id)
        except:
            return Response({'message': f'wrong {instance_id}'}, status=401)

        instance.condition = condition
        if condition == 1:
            fault_info = request.POST.get('fault_info')
            instance.fault_info = fault_info
            response = {'process': f'{-1}'}
        elif condition == 2:
            instance.process = 100
            perspectives_metrics = json.loads(request.data['perspectives_metrics'])
            instance.scores = str(perspectives_metrics)
            for perspective_metrics in perspectives_metrics:
                try:
                    perspective = get_object_or_404(Perspective, name=perspective_metrics['perspective_name'])
                    metrics = perspective_metrics['metrics']
                except:
                    continue
                for metric_all in metrics:
                    metric_value = metric_all['metric_score']
                    metric_name = metric_all['metric_name']
                    try:
                        metric = Metric.objects.get(name=metric_name)
                    except:
                        print('metric here')
                        return Response({'message': f'wrong metric{metric_all}'}, status=400)
                    try:
                        relationship = InstanceMetricPerspectiveRelationship.objects.get(instance=instance,
                                                                                         metric=metric,
                                                                                         perspective=perspective)
                    except:
                        continue

                    if not metric_value:
                        print(metrics)
                    if relationship:
                        relationship.score = metric_value
                        relationship.save()
            response = {'process': f'{100}'}
        elif condition == 0:
            response = {'process': f'{0}'}
        elif condition == 3:
            progress = request.POST.get('progress')
            instance.process = progress
            response = {'process': f'{progress}'}
        else:
            return Response({'message': 'wrong condition'}, status=400)
        instance.save()
        return Response(response, status=200)


class ParameterUpload(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=400)
        parameter = Parameter(user=request.user)
        parameter.save()
        parameter.file = file
        parameter.save()
        return Response({'parameter_id': parameter.id}, status=201)


class InstanceCondition(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        instance_id = request.GET.get('instance_id')
        try:
            instance = ModelInstance.objects.get(id=instance_id, user=request.user)
        except:
            return Response({'message': 'wrong instance id'}, status=400)
        condition = int(instance.condition)
        if condition == 2:
            relationships = InstanceMetricPerspectiveRelationship.objects.filter(instance=instance)
            evaluate_score = {}
            for relationship in relationships:
                perspective = relationship.perspective
                perspective_name = perspective.name
                metric = relationship.metric
                score = relationship.score
                metric_score = {'metric_name': metric.name, 'metric_score': score}
                if perspective_name not in evaluate_score:
                    evaluate_score[perspective_name] = {'perspective_name': perspective_name, 'metrics': [metric_score]}
                else:
                    evaluate_score[perspective_name]['metrics'].append(metric_score)
            return Response({'condition': instance.condition, 'evaluate_score': list(evaluate_score.values())},
                            status=200)
        elif condition == 1:
            return Response({'condition': instance.condition, 'fault': instance.fault_info}, status=200)
        elif condition == 0 or condition == 3:
            return Response({'condition': instance.condition, 'process': instance.process}, status=200)
        else:
            return Response({'message': 'wrong instance condition'}, status=400)
