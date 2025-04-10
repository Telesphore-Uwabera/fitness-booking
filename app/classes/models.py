from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    duration = models.DurationField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='class_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ClassSchedule(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='schedules')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    available_spots = models.PositiveIntegerField()
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.fitness_class.name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):
        if not self.available_spots:
            self.available_spots = self.fitness_class.capacity
        super().save(*args, **kwargs)

    @property
    def is_full(self):
        return self.available_spots == 0

    @property
    def is_past(self):
        return self.end_time < timezone.now() 