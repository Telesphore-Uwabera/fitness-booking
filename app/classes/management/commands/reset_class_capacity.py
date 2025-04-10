from django.core.management.base import BaseCommand
from classes.models import FitnessClass, ClassSchedule

class Command(BaseCommand):
    help = 'Reset all class capacities to 50 and update available spots'

    def handle(self, *args, **options):
        # Update all FitnessClass capacities to 50
        FitnessClass.objects.all().update(capacity=50)
        
        # Update available spots for all class schedules
        for schedule in ClassSchedule.objects.all():
            schedule.available_spots = 50
            schedule.save()
            
        self.stdout.write(
            self.style.SUCCESS('Successfully reset all class capacities to 50')
        ) 