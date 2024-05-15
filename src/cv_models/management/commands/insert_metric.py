from django.core.management.base import BaseCommand
from cv_models.models import Aspect, Perspective, Metric, Task

class Command(BaseCommand):
    help = 'Insert data into Metric'

    def handle(self, *args, **options):
        task_id = 1
        aspect_id = 4
        perspective_id = 1
        
        name = 'gbc'
        description = 'Pándy et al. proposed a novel measure called the Gaussian Bhattacharyya Coefficient (GBC) to evaluate the transferability between a model and a target dataset by measuring the amount of overlap between target classes in the source feature space.'
        
        is_default = 0
        
        metric = Metric(task_id=task_id, aspect_id=aspect_id, perspective_id=perspective_id, name=name, description=description, is_default=is_default)
        
        metric.save()
        
        self.stdout.write(self.style.SUCCESS('Data inserted successfully'))