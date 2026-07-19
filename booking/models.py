import random
import string

from django.conf import settings
from django.db import models


class Train(models.Model):
    train_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    total_seats = models.PositiveIntegerField(default=100)
    fare = models.DecimalField(max_digits=8, decimal_places=2)
    running_days = models.CharField(
        max_length=50,
        default='Mon,Tue,Wed,Thu,Fri,Sat,Sun',
        help_text='Comma separated e.g. Mon,Tue,Wed'
    )

    class Meta:
        ordering = ['departure_time']

    def __str__(self):
        return f"{self.train_number} - {self.name} ({self.source} -> {self.destination})"

    def runs_on(self, weekday_abbr):
        return weekday_abbr in [d.strip() for d in self.running_days.split(',')]

    def booked_seats_for_date(self, journey_date):
        agg = self.bookings.filter(
            journey_date=journey_date, status='CONFIRMED'
        ).aggregate(total=models.Sum('num_seats'))
        return agg['total'] or 0

    def available_seats_for_date(self, journey_date):
        return self.total_seats - self.booked_seats_for_date(journey_date)


def generate_pnr():
    chars = string.ascii_uppercase + string.digits
    while True:
        pnr = ''.join(random.choices(chars, k=10))
        if not Booking.objects.filter(pnr=pnr).exists():
            return pnr


class Booking(models.Model):
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('WAITING', 'Waiting'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='bookings')
    journey_date = models.DateField()
    pnr = models.CharField(max_length=10, unique=True, default=generate_pnr, editable=False)
    num_seats = models.PositiveIntegerField(default=1)
    total_fare = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CONFIRMED')
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-booked_at']

    def __str__(self):
        return f"{self.pnr} - {self.train.name} - {self.user}"


class Passenger(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='passengers')
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    seat_number = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.name} ({self.seat_number})"
