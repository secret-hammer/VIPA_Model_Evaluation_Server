from django.core.management.base import BaseCommand
from cv_models.models import Architecture, Parameter

class Command(BaseCommand):
    help = 'Insert data into Parameter'

    def handle(self, *args, **options):
        user_id = 1
        architecture_id = 8
        
        name = 'vgg16_svhn'
        description = 'vgg16 trained on svhn for 200 epochs selected with the best validation accuracy'
        
        path = '/nfs/xwx/MXPG/checkpoints/vgg16_c100/svhn/best_model.pth'
        is_public = 0
    
        
        parameter = Parameter(name=name, description=description, path=path, is_public=is_public, user_id=user_id, architecture_id=architecture_id)
        
        parameter.save()
        
        self.stdout.write(self.style.SUCCESS('Data inserted successfully'))