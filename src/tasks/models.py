import os

from django.db import models

from cv_models.models import Metric, Task, Architecture, Environment, Perspective, Aspect, Parameter
from datasets.models import Dataset
from users.models import User


class ModelInstance(models.Model):
    # Methods
    def generate_path(self, filename):
        # 根据实例和文件名生成动态路径
        if filename and '.' in filename:
            suffix = filename.rsplit(".", 1)[1]
        unique_filename = f'{self.id}.{suffix}'
        url = f'{self.user.id}/{self.__class__.__name__}/{unique_filename}'
        # 判断存储路径中是否存在文件
        if os.path.exists(os.path.join('media', url)):
            # 删除存储路径中的文件
            os.remove(os.path.join('media', url))
        return url

    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    architecture = models.ForeignKey(Architecture, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    aspect = models.ForeignKey(Aspect, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, null=True, blank=True)
    fault_info = models.TextField(null=True, blank=True)
    scores = models.CharField(max_length=255, null=True, blank=True, default='')

    upload_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    condition = models.IntegerField(default=0)
    process = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.id) + ' ' + str(self.condition)


class InstanceMetricPerspectiveRelationship(models.Model):
    instance = models.ForeignKey(ModelInstance, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    perspective = models.ForeignKey(Perspective, on_delete=models.CASCADE)
    score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.instance.id) + ' ' + self.metric.name + ' ' + str(self.score)
