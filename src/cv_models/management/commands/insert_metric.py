from django.core.management.base import BaseCommand
from cv_models.models import Aspect, Perspective, Metric, Task

class Command(BaseCommand):
    help = 'Insert data into Metric'

    def handle(self, *args, **options):
        task_id = 1
        aspect_id = 1
        perspective_id = 4
        
        name = 'recall'
        description = 'Recall, also known as sensitivity or true positive rate, is a metric used to evaluate the performance of classification models. It specifically measures the ability of the model to correctly identify positive samples out of all the actual positive samples in a dataset. Recall is calculated as the ratio of true positive predictions to the sum of true positives and false negatives, using the formula: recall = true positives (true positives + false negatives).'
        
        is_default = 0
        
        metric = Metric(task_id=task_id, aspect_id=aspect_id, perspective_id=perspective_id, name=name, description=description, is_default=is_default)
        
        metric.save()
        
        self.stdout.write(self.style.SUCCESS('Data inserted successfully'))