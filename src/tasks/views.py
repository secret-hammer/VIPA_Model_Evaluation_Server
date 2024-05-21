import json

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ME.settings import EVALUATE_IP_PORT, MEDIA_ROOT
from datasets.models import Dataset
from .models import Metric, ModelInstance, InstanceMetricPerspectiveRelationship
from cv_models.models import Architecture, Task, Environment, Perspective, Aspect, Parameter
import requests
import os


# Create your views here.


class ResultView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        instance_id = request.data.get('instance_id')
        dataset_id = request.data.get('dataset_id')
        task_id = request.data.get('task_id')
        aspect_id = request.data.get('aspect_id')
        architecture_id = request.data.get('architecture_id')
        parameter_id = request.data.get('parameter_id')
        condition = request.data.get('condition')
        
        try:
            instances = ModelInstance.objects.filter(user=user)
            if instance_id:
                instances = instances.filter(id=instance_id)
            if dataset_id:
                instances = instances.filter(dataset_id=dataset_id)
            if task_id:
                instances = instances.filter(task_id=task_id)
            if aspect_id:
                instances = instances.filter(aspect_id=aspect_id)
            if architecture_id:
                instances = instances.filter(architecture_id=architecture_id)
            if parameter_id:
                instances = instances.filter(parameter_id=parameter_id)
            if condition:
                instances = instances.filter(condition=condition)
        except Exception as e:
            return Response({'message': str(e)}, status=400)
        response = []

        for instance in instances:
            instance_response = {
                'instance_id' : instance.id,
                'architecture_name' : instance.architecture.name,
                'paper_link' : instance.architecture.paper_link,
                'code_link' : instance.architecture.code_link,
                'user_name' : instance.user.username,
                'task_name' : instance.task.name,
                'aspect_name' : instance.aspect.name,
                'dataset_name' : instance.dataset.name,
                'parameter_name' : instance.parameter.name,
                'environment_name' : instance.environment.name,
                'condition' : instance.condition
            }
            if instance.condition == 1:
                instance_response['process'] = instance.process
            elif instance.condition == 2:
                relationships = InstanceMetricPerspectiveRelationship.objects.filter(instance=instance)
                evaluate_score = {}
                for relationship in relationships:
                    metric = relationship.metric
                    score = relationship.score
                    scores = {'metric_name': metric.name, 'metric_score': score}
                    perspective = relationship.perspective
                    perspective_name = perspective.name
                    if perspective_name not in evaluate_score.keys():
                        evaluate_score[perspective_name] = {'perspective_name': perspective_name, 'metrics': [scores]}
                    else:
                        evaluate_score[perspective_name]['metrics'].append(scores)
                instance_response['evaluate_score'] = list(evaluate_score.values())
            elif instance.condition == 3:
                instance_response['fault_info'] = instance.fault_info
            response.append(instance_response)    
            
        return Response(response, status=200)

# 启动评估任务
class Evaluation(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        architecture_id = request.data.get('architecture_id')
        task_id = request.data.get('task_id')
        dataset_id = request.data.get('dataset_id')
        metric_ids = request.data.get('metric_ids')
        aspect_id = request.data.get('aspect_id')
        parameter_id = request.data.get('parameter_id')
        environment_id = request.data.get('environment_id')
        try:
            architecture = Architecture.objects.get(id=architecture_id)
            task = Task.objects.get(id=task_id)
            dataset = Dataset.objects.get(id=dataset_id)
            environment = Environment.objects.get(id=environment_id)
            aspect = Aspect.objects.get(id=aspect_id)
            parameter = Parameter.objects.get(id=parameter_id)
        except:
            return Response({
                'message': f'Invalid arch {architecture_id}/task {task_id}/dataset {dataset_id}/environment {environment_id}/aspect {aspect_id}/parameter id{parameter_id}'},
                status=400)
        
        # 初始化条件为0，表示当前任务没有开始
        instance = ModelInstance(user=request.user, architecture=architecture, task=task, dataset=dataset,
                                 environment=environment, aspect=aspect, parameter=parameter, condition=0)
        instance.save()
        
        # 构建任务实例和评估指标的关系
        metric_id_names = []
        for metric_id in metric_ids:
            try:
                metric = Metric.objects.get(id=metric_id)
                assert metric.aspect == aspect and metric.task == task
                
                metric_id_names.append({'id': metric.id, 'name': metric.name})
                
                relationship = InstanceMetricPerspectiveRelationship(instance=instance, metric=metric, perspective_id=metric.perspective_id)
                relationship.save()
            except Exception as e:
                return Response({'message': f'{str(e)}'}, status=400)
                
        model_name = instance.architecture.name
        dataset_name = instance.dataset.name
        checkpoint_path = instance.parameter.path
        task_name = instance.task.name
        task_type = instance.task.id
        environment = instance.environment.name
        aspect = instance.aspect.name
        task_modelinstance_id = instance.id
        
        json_kwargs = {
            "model_name": model_name,
            "dataset_name": dataset_name,
            "checkpoint_path": checkpoint_path,
            "task_name": task_name,
            "task_type": task_type,
            "environment": environment,
            "aspect": aspect,
            "metrics": metric_id_names,
            "task_modelinstance_id": task_modelinstance_id
        }
        
        # 发起任务请求
        response = requests.post(url="http://10.214.242.156:5002/api/task/add", json=json_kwargs)
        
        if response.status_code == 200:
            return Response({'instance_id': instance.id, 'message': 'Evaluation task successfully start  ' + json.dumps(json_kwargs)}, status=200)
        else:
            return Response({'message': 'Evaluation fail to start'}, status=400)


# 内部同步接口
class EvaluationProcess(APIView):
    def post(self, request):
        instance_id = int(request.data['instance_id'])
        condition = int(request.data['condition'])
        
        try:
            instance = ModelInstance.objects.get(id=instance_id)
        except:
            return Response({'message': f'wrong {instance_id}'}, status=401)


        instance.condition = condition
        response = {}
        try: 
            if condition == 0:
                # 清空process和score
                instance.process = 0
                instance.scores = ''
                response = {'message': 'Set evaluation task to waiting state'}
            elif condition == 1:
                response = {'message': 'Set evaluation task to processing state'} 
            elif condition == 2:
                instance.process = 1
                metric_scores = request.data.get('metric_scores')
                print(metric_scores)
                for metric_score in metric_scores:
                    metric_id = metric_score['metric_id']
                    score = metric_score['score']
                    try:
                        metric = Metric.objects.get(id=metric_id)
                    except Exception as e:
                        return Response({'message': str(e)}, status=400)
                    
                    try:
                        relationship = InstanceMetricPerspectiveRelationship.objects.get(instance=instance, metric_id=metric_id)
                    except:
                        continue
                    relationship.score = score
                    relationship.save()
                
            elif condition == 3:
                fault_info = request.data.get('fault_info')
                instance.fault_info = fault_info
                instance.process = 1
                response = {'message': 'Set evaluation task to fault state'}
            
            else:
                return Response({'message': 'unknown condition'}, status=400)
            
            instance.save()        
        except Exception as e:
            return Response({'message': str(e)}, status=400)
        
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
