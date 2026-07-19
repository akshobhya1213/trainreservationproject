from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegisterForm, TrainSearchForm
from .models import Booking, Passenger, Train

WEEKDAY_ABBR = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


def home(request):
    form = TrainSearchForm()
    return render(request, 'booking/home.html', {'form': form})


def search_trains(request):
    trains = []
    form = TrainSearchForm(request.GET or None)
    journey_date = None
    if form.is_valid():
        source = form.cleaned_data['source'].strip()
        destination = form.cleaned_data['destination'].strip()
        journey_date = form.cleaned_data['journey_date']
        weekday = WEEKDAY_ABBR[journey_date.weekday()]

        qs = Train.objects.filter(
            source__icontains=source,
            destination__icontains=destination,
        )
        for train in qs:
            if train.runs_on(weekday):
                trains.append({
                    'train': train,
                    'available': train.available_seats_for_date(journey_date),
                })
    return render(request, 'booking/search_results.html', {
        'form': form, 'trains': trains, 'journey_date': journey_date,
    })


@login_required
def book_train(request, train_id):
    train = get_object_or_404(Train, id=train_id)
    journey_date_str = request.GET.get('date') or request.POST.get('journey_date')
    if not journey_date_str:
        messages.error(request, 'Please select a journey date first.')
        return redirect('home')
    journey_date = datetime.strptime(journey_date_str, '%Y-%m-%d').date()
    available = train.available_seats_for_date(journey_date)

    num_passengers = int(request.POST.get('num_passengers', request.GET.get('num_passengers', 1)))
    show_passenger_form = 'confirm_count' in request.POST or 'num_passengers' in request.GET

    if request.method == 'POST' and 'submit_booking' in request.POST:
        names = request.POST.getlist('passenger_name[]')
        ages = request.POST.getlist('passenger_age[]')
        genders = request.POST.getlist('passenger_gender[]')
        count = len(names)

        if count < 1 or any(not n.strip() for n in names):
            messages.error(request, 'Please fill in all passenger details.')
        else:
            with transaction.atomic():
                current_available = train.available_seats_for_date(journey_date)
                status = 'CONFIRMED' if count <= current_available else 'WAITING'
                booking = Booking.objects.create(
                    user=request.user,
                    train=train,
                    journey_date=journey_date,
                    num_seats=count,
                    total_fare=train.fare * count,
                    status=status,
                )
                already_booked = train.booked_seats_for_date(journey_date) - (count if status == 'CONFIRMED' else 0)
                for i in range(count):
                    seat_no = f"S{already_booked + i + 1}" if status == 'CONFIRMED' else ''
                    Passenger.objects.create(
                        booking=booking,
                        name=names[i],
                        age=ages[i] or 0,
                        gender=genders[i] or 'O',
                        seat_number=seat_no,
                    )
            if status == 'CONFIRMED':
                messages.success(request, f'Booking confirmed! Your PNR is {booking.pnr}')
            else:
                messages.warning(request, f'Train is full. You are on the waiting list. PNR: {booking.pnr}')
            return redirect('booking_detail', pnr=booking.pnr)

    passenger_range = range(num_passengers) if show_passenger_form else None

    return render(request, 'booking/book_train.html', {
        'train': train,
        'journey_date': journey_date,
        'available': available,
        'num_passengers': num_passengers,
        'passenger_range': passenger_range,
        'show_passenger_form': show_passenger_form,
    })


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('train')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})


@login_required
def booking_detail(request, pnr):
    booking = get_object_or_404(Booking, pnr=pnr, user=request.user)
    return render(request, 'booking/booking_detail.html', {'booking': booking})


@login_required
def cancel_booking(request, pnr):
    booking = get_object_or_404(Booking, pnr=pnr, user=request.user)
    if request.method == 'POST':
        booking.status = 'CANCELLED'
        booking.save()
        messages.success(request, f'Booking {pnr} has been cancelled.')
        return redirect('my_bookings')
    return render(request, 'booking/cancel_confirm.html', {'booking': booking})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
