from django.shortcuts import render,redirect
from django.urls import reverse
from room.models import Room
from reservation.models import Booking
from .models import Hotel,Comments
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def index(request):
    user_counts=request.session.get('user_count')
    hotels=Hotel.objects.all()
    return render(request,'hotel/index.html',{'hotels':hotels,'user_counts':user_counts})
def filter_locations(request):
    if request.method=='POST':
        location=request.POST['location']
        if len(location)==0:
           messages="Enter location first."
           return render(request,'hotel/index.html',{'messages':messages})
        hotels=Hotel.objects.filter(Q(city=location) | Q(state=location)| Q(country=location))
        if not hotels.exists() and (hotels.first() and hotels.first().name != location):
            messages="No hotels found"
            return render(request,'hotel/index.html',{'messages':messages})
    return render(request,'hotel/index.html',{'hotels':hotels})
def hotel_rooms(request, hotel_id):
    specific_hotel = Hotel.objects.get(id=hotel_id)
    amenities = specific_hotel.amenities.all()  # Retrieve all amenities related to the hotel
    specific_hotel_rooms = Room.objects.filter(hotel=specific_hotel)
    comments = specific_hotel.comment.all().order_by('-created_at')  # Retrieve all comments related to the hotel
    user_count = comments.values_list('email', flat=True).distinct().count()
    for room in specific_hotel_rooms:
        room.room_price_str = str(room.price)
        room.availabilityStatus = not Booking.objects.filter(room_type=room, status__in=['pending', 'confirmed']).exists()
    else:
        specific_hotel_rooms.availabilityStatus=True
    return render(request, 'room/index.html', {'specific_hotel':specific_hotel,'specific_hotel_rooms': specific_hotel_rooms,'amenities':amenities,'user_count':user_count,'comments':comments})
def map_view(request):
    hotelsLoc = Hotel.objects.all() # get all hotels from the database
    context = {'hotelsLoc': hotelsLoc}
    return render(request, 'hotel/index.html', context)


def hotel_comments(request,hotel_id):
       if request.user.is_authenticated:
            specific_hotel = Hotel.objects.get(id=hotel_id)
            comments = specific_hotel.comment.all().order_by('-created_at')  # Retrieve all comments related to the hotel
            user_count = comments.values_list('email', flat=True).distinct().count()
            specific_hotel_rooms = Room.objects.filter(hotel=specific_hotel)
            
            amenities = specific_hotel.amenities.all()  # Retrieve all amenities related to the hotel
           
            if request.method == "POST":
                username=request.POST.get('name')
                email=request.POST.get('email')
                messages = request.POST.get("message")
                if len(username) <=3:
                    return redirect('hotels:hotel_rooms',hotel_id=hotel_id)
                if len(messages) <=20:
                    return redirect('hotels:hotel_rooms',hotel_id=hotel_id)
            # Create and save the comment associated with the specific hotel
                comment = Comments(name=username, email=email, message=messages)
                comment.save()
                # error="Thanks for providing your feedback"
                specific_hotel.comment.add(comment)
                return redirect('hotels:hotel_rooms',hotel_id=hotel_id)
                # return redirect('hotels:hotel_comments')error

                # return render(request, 'room/index.html', {'comments': comments, 'user_count': user_count,'specific_hotel':specific_hotel,'specific_hotel_rooms': specific_hotel_rooms,'amenities':amenities})
            else:
                return render(request, 'room/index.html', {'comments': comments, 'user_count': user_count,'specific_hotel':specific_hotel,'specific_hotel_rooms': specific_hotel_rooms,'amenities':amenities})

       else:
            message = "Please login to post your review"
            return redirect(reverse('users:login') + '?message=' + message)
       
           

    