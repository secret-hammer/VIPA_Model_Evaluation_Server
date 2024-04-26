import os
import zipfile

from django.db import models

from users.models import User


class Architecture(models.Model):
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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

    # Fields
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to=generate_path, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    paper_link = models.URLField(blank=True, null=True)
    code_link = models.URLField(blank=True, null=True)
    is_public = models.BooleanField(default=True)
    model_path = models.CharField(max_length=200, null=True, blank=True)

    # 在save的同时解压缩文件，并删除掉原来的压缩包
    def file_save(self, *args, **kwargs):
        if self.file:
            # 解压文件
            try:
                with zipfile.ZipFile(self.file.path, 'r') as zip_ref:
                    model_py_files = []
                    for file_info in zip_ref.infolist():
                        file_name = file_info.filename
                        if file_name.split('/')[-1] == 'model.py':
                            model_py_files.append(file_name)
                    if model_py_files:
                        shortest = min(model_py_files, key=len)
                        dir_path = shortest.rstrip('model.py')
                        if dir_path:
                            self.model_path = str(self.file.name).rstrip('.zip') + '/' + dir_path + 'model.py'
                        else:
                            self.model_path = str(self.file.name).rstrip('.zip') + '/' + 'model.py'
                    else:
                        self.delete()
                    os.mkdir(self.file.path.rstrip('.zip') + '/')
                    zip_ref.extractall(self.file.path.rstrip('.zip') + '/')
            except:
                self.file.delete()
                self.delete()
            self.file.delete()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# 计算机视觉任务
class Task(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# 环境
class Environment(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# 评估准则
class Metric(models.Model):
    name = models.CharField(max_length=200)
    code_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


# 评估方面
class Aspect(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# 评估视角
class Perspective(models.Model):
    name = models.CharField(max_length=200)
    aspect = models.ForeignKey(Aspect, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# intermediate tables
class TaskArchitectureRelationship(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    architecture = models.ForeignKey(Architecture, on_delete=models.CASCADE)


class MetricPerspectiveTaskRelationship(models.Model):
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    perspective = models.ForeignKey(Perspective, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.metric.name + '   ' + self.perspective.name + '   ' + self.task.name
