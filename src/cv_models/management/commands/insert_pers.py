from django.core.management.base import BaseCommand
from cv_models.models import Aspect, Perspective

class Command(BaseCommand):
    help = 'Insert data into Perspective'

    def handle(self, *args, **options):
        aspect_id = 1
        name = 'Accuracy'
        
        perspective = Perspective(name=name, aspect_id=aspect_id)
        
        perspective.save()
        
        self.stdout.write(self.style.SUCCESS('Data inserted successfully'))