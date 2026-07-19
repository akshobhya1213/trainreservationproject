from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_trains, name='search_trains'),
    path('book/<int:train_id>/', views.book_train, name='book_train'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<str:pnr>/', views.booking_detail, name='booking_detail'),
    path('booking/<str:pnr>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('register/', views.register, name='register'),
]
