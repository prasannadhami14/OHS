from django.urls import path
from . import views
app_name = 'reserve'
urlpatterns = [
    path('book_now/<str:room_number>/<str:room_price>',views.book_now,name="book_now"),
    path('reservation_card',views.reservation_card,name="reservation_card"),
    path('mail_reservation/',views.send_confirmation,name="mail_reservation")
]

