from django.contrib import admin
from .models import Dataset,TaskDatasetRelationship


admin.site.register(Dataset)
admin.site.register(TaskDatasetRelationship)