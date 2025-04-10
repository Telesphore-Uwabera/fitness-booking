from django.core.management.base import BaseCommand
from classes.models import ClassSchedule, FitnessClass
from django.utils import timezone

class Command(BaseCommand):
    help = 'Reset available spots for all classes to maximum capacity'

    def handle(self, *args, **options):
        # Update all fitness classes to have capacity of 20
        FitnessClass.objects.all().update(capacity=20)
        
        # Update all future class schedules to have 20 available spots
        future_schedules = ClassSchedule.objects.filter(start_time__gte=timezone.now())
        updated_count = future_schedules.update(available_spots=20)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully reset {updated_count} class schedules to 20 available spots'
            )
        ) 