# RailBook - Django Train Reservation System

A full-stack train ticket booking system built with Django (backend + server-rendered
frontend using Bootstrap 5).

## Features

- User registration & login (Django auth)
- Search trains by source, destination, and date (with weekly running-day logic)
- Live seat availability per train per date
- Multi-passenger booking (name, age, gender) with dynamic passenger form
- Automatic PNR generation, fare calculation, and waiting-list handling when a
  train is full
- "My Bookings" dashboard + ticket detail view
- Booking cancellation
- Django admin panel to manage trains and bookings, with inline passenger editing
- Sample train data seed command

## Project Structure

```
trainres/
├── manage.py
├── trainres/            # project settings, urls
├── booking/              # main app: models, views, forms, admin, urls
│   └── management/commands/seed_trains.py
├── templates/            # Bootstrap-based HTML templates
│   ├── base.html
│   ├── booking/
│   └── registration/
└── static/
```

## Setup

1. Create a virtual environment and install Django:
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install django
   ```

2. Apply migrations:
   ```bash
   python manage.py migrate
   ```

3. Seed sample trains (optional but recommended):
   ```bash
   python manage.py seed_trains
   ```

4. Create an admin account:
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Visit:
   - `http://127.0.0.1:8000/` — search & book trains
   - `http://127.0.0.1:8000/admin/` — manage trains/bookings as admin

## How Booking Works

1. Search by source, destination, and date on the home page.
2. Results show live seat availability, computed as
   `total_seats - sum(confirmed bookings for that train+date)`.
3. Choose number of passengers, then fill in each passenger's name/age/gender.
4. On submit, the system:
   - Generates a unique 10-character PNR
   - Calculates total fare (`train.fare × passengers`)
   - Marks the booking `CONFIRMED` if seats are available, otherwise `WAITING`
   - Assigns seat numbers (e.g. `S1`, `S2`) for confirmed bookings
5. Users can view all bookings under "My Bookings" and cancel any active booking.

## Notes / Next Steps for Production

- Set `DEBUG = False` and configure `ALLOWED_HOSTS` in `trainres/settings.py`.
- Switch from SQLite to PostgreSQL/MySQL for production.
- Add payment gateway integration before charging real fares.
- Add per-class seating (Sleeper/AC) if needed — currently a single fare/seat
  pool per train.
