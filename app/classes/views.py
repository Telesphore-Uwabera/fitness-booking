from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import FitnessClass
from bookings.models import Booking

def class_list(request):
    classes = FitnessClass.objects.all()
    return render(request, 'classes/class_list.html', {'classes': classes})

def class_detail(request, class_id):
    fitness_class = get_object_or_404(FitnessClass, id=class_id)
    return render(request, 'classes/class_detail.html', {'class': fitness_class})

@login_required
def book_class(request, class_id):
    fitness_class = get_object_or_404(FitnessClass, id=class_id)
    if request.method == 'POST':
        Booking.objects.create(
            user=request.user,
            fitness_class=fitness_class
        )
        return redirect('bookings:booking_list')
    return render(request, 'classes/book_class.html', {'class': fitness_class}) 