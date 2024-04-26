import os

from django.db import models
from cv_models.models import Task
from users.models import User


class Dataset(models.Model):
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Methods
    def __str__(self):
        return self.name

    def generate_path(self, filename):
        # 根据实例和文件名生成动态路径
        if filename and '.' in filename:
            suffix = filename.rsplit(".", 1)[1]
            unique_filename = f'{filename}.{suffix}'
        else:
            unique_filename = filename
        url = f'{self.user.id}/datasets/{unique_filename}'
        if os.path.exists(os.path.join('media', url)):
            # 删除存储路径中的文件
            os.remove(os.path.join('media', url))
        return url

    # Fields
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    file = models.FileField(upload_to=generate_path, blank=True, null=True)
    paper_link = models.URLField(blank=True, null=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    principal = models.CharField(max_length=255, default='')


class TaskDatasetRelationship(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
