
from django.core.management.base import BaseCommand

from booking.models import Train

SAMPLE_TRAINS = [
    dict(train_number='12627', name='Karnataka Express', source='Bangalore', destination='Delhi',
         departure_time='20:00', arrival_time='05:30', total_seats=80, fare=1450.00,
         running_days='Mon,Wed,Fri,Sun'),
    dict(train_number='12007', name='Shatabdi Express', source='Bangalore', destination='Chennai',
         departure_time='06:00', arrival_time='11:00', total_seats=60, fare=850.00,
         running_days='Mon,Tue,Wed,Thu,Fri,Sat,Sun'),
    dict(train_number='16022', name='Kaveri Express', source='Bangalore', destination='Chennai',
         departure_time='21:15', arrival_time='05:45', total_seats=100, fare=550.00,
         running_days='Mon,Tue,Wed,Thu,Fri,Sat,Sun'),
    dict(train_number='12296', name='Sanghamitra Express', source='Bangalore', destination='Mumbai',
         departure_time='11:00', arrival_time='13:30', total_seats=90, fare=1200.00,
         running_days='Tue,Thu,Sat'),
    dict(train_number='12578', name='Ganga Express', source='Delhi', destination='Bangalore',
         departure_time='14:20', arrival_time='23:50', total_seats=75, fare=1600.00,
         running_days='Mon,Wed,Fri'),
    dict(train_number='12639', name='Brindavan Express', source='Chennai', destination='Bangalore',
         departure_time='07:15', arrival_time='12:30', total_seats=70, fare=500.00,
         running_days='Mon,Tue,Wed,Thu,Fri,Sat,Sun'),
    dict(train_number='11302', name='Udyan Express', source='Mumbai', destination='Bangalore',
         departure_time='08:05', arrival_time='10:35', total_seats=95, fare=1150.00,
         running_days='Mon,Tue,Wed,Thu,Fri,Sat,Sun'),
    dict(train_number='12649', name='Sampark Kranti', source='Bangalore', destination='Delhi',
         departure_time='06:45', arrival_time='06:00', total_seats=85, fare=1550.00,
         running_days='Sat'),
]


class Command(BaseCommand):
    help = 'Seed the database with sample train data'

    def handle(self, *args, **options):
        created_count = 0
        for data in SAMPLE_TRAINS:
            _, created = Train.objects.get_or_create(
                train_number=data['train_number'], defaults=data
            )
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(
            f'Seeded {created_count} new trains (skipped {len(SAMPLE_TRAINS) - created_count} existing).'
        ))
