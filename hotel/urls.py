from django.urls import path
from django.urls import path,include

from . import views
app_name = "hotels"

urlpatterns = [
    path('',views.index, name="index"),
    path('filter_location/',views.filter_locations, name="filter_location"),
    path('hotel/<int:hotel_id>/rooms/', views.hotel_rooms, name='hotel_rooms'),  # New path for hotel rooms
    path('hotel_room/<int:hotel_id>/',views.hotel_comments,name='hotel_comments'), # New path for


]
