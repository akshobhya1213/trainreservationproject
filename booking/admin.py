from django.contrib import admin

from .models import Booking, Passenger, Train


class PassengerInline(admin.TabularInline):
    model = Passenger
    extra = 0


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('train_number', 'name', 'source', 'destination',
                     'departure_time', 'arrival_time', 'total_seats', 'fare')
    search_fields = ('train_number', 'name', 'source', 'destination')
    list_filter = ('source', 'destination')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('pnr', 'user', 'train', 'journey_date', 'num_seats', 'total_fare', 'status', 'booked_at')
    list_filter = ('status', 'journey_date')
    search_fields = ('pnr', 'user__username')
    inlines = [PassengerInline]


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'seat_number', 'booking')
