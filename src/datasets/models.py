import os

from django.db import models
from cv_models.models import Task
from users.models import User


class Dataset(models.Model):
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Fields
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    path = models.CharField(max_length=255, blank=True, null=True)
    paper_link = models.URLField(blank=True, null=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    principal = models.CharField(max_length=255, default='')
    
    
    # Methods
    def __str__(self):
        return self.name
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'path': self.path,
            'paper_link': self.paper_link,
            'upload_time': self.upload_time,
            'update_time': self.update_time,
            'is_public': self.is_public,
            'principal': self.principal
        }

    
    


class TaskDatasetRelationship(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
