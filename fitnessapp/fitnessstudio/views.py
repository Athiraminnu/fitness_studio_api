import json
from django.core.validators import validate_email
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Class, Bookings
from .serializer import ClassSerializer, BookingsSerializer

# Create your views here.

@api_view(['GET'])
def classes(request):
    all_classes = Class.objects.all() #fetches all the data
    classes_serializer = ClassSerializer(all_classes, many=True) # serializes the data into Python native types ready for JSON rendering
    return Response({'classes': classes_serializer.data})


@api_view(['POST'])
def bookings(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            clientname = data.get('client_name')   # get the client name from the request
            clientemail = data.get('client_email')   # get the client email from the request
            class_to_book = data.get('class_id')   # get the class ID from the request

            if not all([clientname, clientemail, class_to_book]):   # check if all required fields are provided
                return JsonResponse({'Error': 'Missing required fields'}, status=400)

            try:
                validate_email(clientemail)   # validate the email format
            except ValidationError:
                return Response({'Error': 'Invalid email format.'}, status=400)

            try:
                class_data = Class.objects.get(id=class_to_book)     # retrieve the class instance by ID(raises exception if not found)
                available_slots = class_data.available_slots    # get the number of available slots for the class

                      #check if this email already booked this class
                already_booked = Bookings.objects.filter(
                    client_email=clientemail,
                    class_id=class_data
                ).exists()

                if already_booked:
                    return JsonResponse({'Error': 'You have already booked a slot for this class.'}, status=409)

                if available_slots > 0:   # check if slots are available
                    # create a new booking
                    new_booking = Bookings.objects.create(
                        client_name=clientname,
                        client_email=clientemail,
                        class_id=class_data
                    )
                    class_data.available_slots -= 1    # reduce available slots by 1 after successful booking
                    class_data.save()    # save the updated class data

                    # return a success response with booking details
                    return JsonResponse({
                        'message': "Booking successfully!!",
                        'booking_id': new_booking.id,
                        'class_name': class_data.name
                    })
                else:    # return error if no slots are available
                    return JsonResponse({'Error': 'No available slots for this class'}, status=400)

            except Class.DoesNotExist:    # return error if the class does not exist
                return JsonResponse({'Error': 'Class not found'}, status=404)

        except json.JSONDecoderError:    # return error if the input is not valid JSON
            return JsonResponse({'Error': 'Invalid JSON format'}, status=400)

    return JsonResponse({'Error': 'Only POST requests are allowed'}, status=405)


@api_view(['GET'])
def bookingData(request):
    email = request.GET.get('email')    # get the email parameter from the URL query string
    if not email:    # return an error if email is not provided
        return Response({'Error': 'Email is required.'}, status=400)
    else:
        try:
            validate_email(email)
        except ValidationError:     # return an error if the email format is invali
            return Response({'error': 'Invalid email format.'}, status=400)

    bookings_data = Bookings.objects.filter(client_email=email)    # filter Bookings matching the given email
    bookings_data_serializer = BookingsSerializer(bookings_data, many=True)    # serialize the Bookings into Python native types (for JSON response)
    return Response({'bookings': bookings_data_serializer.data})
