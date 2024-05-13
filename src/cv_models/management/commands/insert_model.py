from django.core.management.base import BaseCommand
from cv_models.models import Architecture

class Command(BaseCommand):
    help = 'Insert data into Dataset'

    def handle(self, *args, **options):
        user_id = 1
        task_id = 1
        
        name = 'seresnet50'
        path = '/disk1/xwx/MXPG/algorithm_tasks/classification/models/cifar100/senet.py'
        description = 'SE-Net introduces the "Squeeze-and-Excitation" (SE) block, which recalibrates feature responses by modeling channel interdependencies. These blocks can be stacked to create SENet architectures that perform well across various datasets. SE blocks improve the performance of existing CNNs with minimal additional computational cost.'
        paper_link = 'https://github.com/xmu-xiaoma666/External-Attention-pytorch'
        code_link = 'https://github.com/pytorch/vision'
        is_public = 0
        
        architecture = Architecture(name=name, path=path, description=description, paper_link=paper_link, code_link=code_link, is_public=is_public, user_id=user_id, task_id=task_id)
        
        architecture.save()
        

        self.stdout.write(self.style.SUCCESS('Data inserted successfully'))