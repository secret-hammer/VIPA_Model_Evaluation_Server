from django.core.management.base import BaseCommand
from datasets.models import Dataset, TaskDatasetRelationship

class Command(BaseCommand):
    help = 'Insert data into Dataset'

    def handle(self, *args, **options):
        name = 'cifar100'
        description = 'The CIFAR-100 dataset (Canadian Institute for Advanced Research, 100 classes) is a subset of the Tiny Images dataset and consists of 60000 32x32 color images. The 100 classes in the CIFAR-100 are grouped into 20 superclasses. There are 600 images per class.'
        paper_link = 'https://www.cs.toronto.edu/~kriz/learning-features-2009-TR.pdf'
        is_public = 0
        user_id = 1
        task_id = 1
        
        dataset = Dataset(name=name, description=description, paper_link=paper_link, is_public=is_public, user_id=user_id)
        
        dataset.save()
        
        task_dataset_relation = TaskDatasetRelationship(task_id=task_id, dataset_id=dataset.id)
        task_dataset_relation.save()

        self.stdout.write(self.style.SUCCESS('Data inserted successfully'))