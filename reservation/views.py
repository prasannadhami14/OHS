
from datetime import datetime
from decimal import Decimal
from django.conf import settings
from django.shortcuts import  render,redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from .models import Booking
from room.models import Room
from hotel.models import Hotel
from django.contrib.auth.decorators import login_required


# Create your views here.
def book_now(request,room_number,room_price):
    if request.user.is_authenticated:
        user=request.user
        user_name=user.first_name+" "+user.last_name
        email=user.email       
        return render(request,'reservation/index.html',{"user_name":user_name,"email":email,'room_number':room_number,'room_price':room_price})
    else:
        message="Please login to reserve a room!!!!" 
        return render(request,'customer/login.html',{'message':message})
@login_required
def send_confirmation(request):
            myuser=request.user
            name=myuser.first_name
            error=None

            if myuser.is_authenticated:
             if request.method == 'POST':
                user=name + myuser.last_name
                phone=request.POST['phone']
                price=request.POST.get('price')
                date=request.POST["daterange"]
                adult_count=request.POST["adult_count"]
                child_count=request.POST["child_count"]
                date_range = request.POST.get('daterange')
                email=myuser.email
                selected_room = request.POST.get("room_no")
                if 'selected_room' in request.POST:
                    selected_room = request.POST["room_no"]
                room_number_exists = Room.objects.filter(room_number=selected_room).exists()
                if not room_number_exists:
                   # Handle the case where the selected room number is not valid
                   error = "The selected room number is not valid. Please select a valid room number."
                   return render(request, 'reservation/index.html', {'error': error})
                rooms = Room.objects.get(room_number=selected_room)  # Retrieve the Room object with the desired room number
                if adult_count is None and child_count is None:
                      error="please select a number adult and child!!!! "
                      return render(request,'reservation/index.html',{'error':error})
                else:
                    # Split the date range string into start_date and end_date
                    start_date_str, end_date_str = date_range.split(' - ')
                    # Parse the start_date and end_date strings into datetime objects
                    start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
                    end_date = datetime.strptime(end_date_str, '%d/%m/%Y')
                    formatted_start_date = start_date.strftime('%Y-%m-%d')
                    formatted_end_date = end_date.strftime('%Y-%m-%d')
                    # print(rooms)
                    # print(room_number_exists)

                    # Calculate the number of days between start_date and end_date
                    # difference = formatted_end_date - formatted_start_date 
                    difference = end_date - start_date 

                    number_of_nights = difference.days-1
                    if price is not None:
                         total_price = number_of_nights * Decimal(price)
                    else:
                         total_price = price
                    # print(total_price)
                    if error is None:
                        booked=Booking(user=user,
                                    contact=phone,
                                    email=email,
                                    room_type=rooms,
                                    checkInDate=formatted_start_date,
                                    checkOutDate=formatted_end_date,
                                    totalPrice=total_price,
                                    status="pending"
                                    )
                        booked.save()

                        if booked.status == "pending" or booked.status == "confirmed":
                            rooms.availabilityStatus=False
                        if booked.status == "cancled":
                            rooms.availabilityStatus=True
                        rooms.save()

                        # email for registration    

                        subject="Room Confirmation!!!"
                        message = f"Hello {name.title()},\n\nWelcome to {rooms.hotel}!\nYour booking for room number {selected_room} of {rooms} type from {date} has been reserved.\nPlease contact hotel before your reservation expires to confirm you reservation.\n\nAdult Count: {adult_count}\nChildren Count: {child_count}\n\nTotal bill amount : RS.{total_price} \nPayment Type:Pay on property\n\nThank you for visiting us.\nFor any queries contact us:\nMail: infoapps@gmail.com\nPhone: 01-4562398"
                        from_email=settings.EMAIL_HOST_USER
                        to_list=[myuser.email]
                        send_mail(subject,message,from_email,to_list,fail_silently=True)
                        messages.success(request,"Check your email address \nRooms reservations details have been sent.")
                        return redirect(reverse('hotels:index'))
            else:
                   message="Please login to reserve a room!!!!" 
                   return render(request,"customer/login.html",{'message':message})
            
def reservation_card(request):
    return render(request,'reservation/reservationCard.html')
