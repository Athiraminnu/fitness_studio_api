import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Class, Bookings
from .serializer import ClassSerializer, BookingsSerializer


# Create your views here.

@api_view(['GET'])
def dashboard(request):
    all_classes = Class.objects.all()
    classes_serializer = ClassSerializer(all_classes, many=True)
    return Response({'classes': classes_serializer.data})


@api_view(['POST'])
def bookings(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            clientname = data.get('client_name')
            clientemail = data.get('client_email')
            class_to_book = data.get('class_id')

            if not all([clientname, clientemail, class_to_book]):
                return JsonResponse({'Error': 'Missing required fields'}, status=400)

            try:
                class_data = Class.objects.get(id=class_to_book)
                available_slots = class_data.available_slots

                if available_slots > 0:
                    new_booking = Bookings.objects.create(
                        client_name=clientname,
                        client_email=clientemail,
                        class_id=class_data
                    )
                    class_data.available_slots -= 1
                    class_data.save()

                    return JsonResponse({
                        'message': "Booking successfully!!",
                        'booking_id': new_booking.id,
                        'class_name': class_data.name
                    })
                else:
                    return JsonResponse({'Error': 'No available slots for this class'}, status=400)

            except Class.DoesNotExist:
                return JsonResponse({'Error': 'Class not found'}, status=404)

        except json.JSONDecoderError:
            return JsonResponse({'Error': 'Invalid JSON format'}, status=400)

    return JsonResponse({'Error': 'Only POST requests are allowed'}, status=405)


@api_view(['GET'])
def bookingData(request):
    email = request.GET.get('email')
    if not email:
        return Response({'Error': 'Email is required.'}, ststus=400)
    bookings_data = Bookings.objects.filter(client_email=email)
    bookings_data_serializer = BookingsSerializer(bookings_data, many=True)
    return Response({'bookings': bookings_data_serializer.data})
