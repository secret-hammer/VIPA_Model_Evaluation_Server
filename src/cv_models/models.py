import os
import zipfile

from django.db import models

from users.models import User

# 计算机视觉任务
class Task(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Architecture(models.Model):
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)

    # Fields
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    paper_link = models.URLField(blank=True, null=True)
    code_link = models.URLField(blank=True, null=True)
    is_public = models.BooleanField(default=True)
    

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
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'path': self.path,
            'description': self.description,
            'upload_time': self.upload_time,
            'update_time': self.update_time,
            'paper_link': self.paper_link,
            'code_link': self.code_link,
            'is_public': self.is_public,
            'user': self.user.username,
            'task': self.task.id
        }

# 模型权重
class Parameter(models.Model):
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    architecture = models.ForeignKey(Architecture, on_delete=models.CASCADE)
    # Fields
    name = models.CharField(max_length=200, blank=True, null=True)
    train_dataset_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    path = models.CharField(max_length=255, null=False)
    upload_time = models.DateTimeField(auto_now_add=True, null=True)
    is_public = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'train_dataset_name' : self.train_dataset_name,
            'description': self.description,
            'path': self.path,
            'upload_time': self.upload_time,
            'is_public': self.is_public,
            'user': self.user.username,
            'architecture': self.architecture.name
        }
    


# 环境
class Environment(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# 评估性能
class Aspect(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# 某个性能下的评估视角
class Perspective(models.Model):
    name = models.CharField(max_length=200)
    aspect = models.ForeignKey(Aspect, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# 评估准则
class Metric(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    aspect = models.ForeignKey(Aspect, on_delete=models.CASCADE, null=True)
    perspective = models.ForeignKey(Perspective, on_delete=models.CASCADE, null=True)
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(default=False)
    

    def __str__(self):
        return self.metric.name + '_' + self.aspect.name + '_' + self.perspective.name + '_' + self.task.name
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_default': self.is_default,
            'task': self.task.name,
            'aspect': self.aspect.name,
            'perspective': self.perspective.name
        }
