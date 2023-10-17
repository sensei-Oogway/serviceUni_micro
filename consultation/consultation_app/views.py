from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from .models import GP, Appointment
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from .serializers import GpSerializer

@api_view(['POST'])
def book_appointment(request):
    """
    Book a new appointment with a GP.
    """
    if request.method == 'POST':
        try:
            gp_id = request.data['gp_id']
            user_id = request.data['user_id']
            time_stamp_str = request.data['time_stamp']
            
            # Check if the GP and User exist
            gp = GP.objects.get(pk=gp_id)
            
            # Check if the GP is available for the given timestamp
            # appointment_time = datetime.fromisoformat(time_stamp_str)
            # existing_appointments = gp.appointment_ids.filter(time_stamp=appointment_time)
            
            # if existing_appointments.exists():
            #     return Response({"detail": "GP is not available at the specified time."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create a new appointment
            appointment = GP.add_appointment_to_gp(gp_id, user_id, time_stamp_str)
            
            if appointment:
                return Response({"detail": "Appointment booked successfully.", "appointment_id": appointment.id}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Unable to book the appointment."}, status=status.HTTP_400_BAD_REQUEST)
        
        except GP.DoesNotExist:
            return Response({"detail": "GP not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def view_slots(request, gp_id):
    """
    View available slots for a specific GP.
    """
    try:
        gp = get_object_or_404(GP, pk=gp_id)
        
        # Get the current date and time
        current_datetime = datetime.now()

        # Filter appointments that are in the future and associated with the GP
        appointments = Appointment.objects.filter(
            time_stamp__gte=current_datetime,
            id__in=gp.appointment_ids.all().values_list('id', flat=True)
        )

        # Serialize the appointments to JSON
        serialized_appointments = [{"id": appointment.id, "time_stamp": appointment.time_stamp} for appointment in appointments]

        return Response(serialized_appointments, status=status.HTTP_200_OK)

    except GP.DoesNotExist:
        return Response({"detail": "GP not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def view_appointments(request, user_id):
    """
    View appointments for a specific user including GP details.
    """
    try:
        # Filter appointments associated with the user
        appointments = Appointment.objects.filter(user=user_id)

        serialized_appointments = []
        
        for appointment in appointments:
            gp = GP.objects.filter(appointment_ids=appointment).first()
            if gp:
                appointment_data = {
                    "id": appointment.id,
                    "time_stamp": appointment.time_stamp,
                    "gp": {
                        "id": gp.id,
                        "name": gp.name,
                        "description": gp.description,
                    }
                }
                serialized_appointments.append(appointment_data)

        return Response(serialized_appointments, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_all_gp(request):
    """
    Get all medicines.
    """
    try:
        gp = GP.get_all_gp()

        # Serialize the medicines to JSON
        serialized_gp = [{"id": gp.id, "name": gp.name, "description": gp.description, "slots": gp.slots} for gp in gp]

        return Response(serialized_gp, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
def update_appointment(request, gp_id, appointment_id):
    """
    Update an appointment for a specific GP.
    """
    try:
        gp = get_object_or_404(GP, pk=gp_id)
        appointment = get_object_or_404(Appointment, pk=appointment_id)

        # Check if the appointment is associated with the GP
        if appointment in gp.appointment_ids.all():
            # Update the appointment data
            new_time_stamp = request.data.get('time_stamp')
            if new_time_stamp:
                appointment.time_stamp = datetime.fromisoformat(new_time_stamp)
                appointment.save()
                return Response({"detail": "Appointment updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Appointment not found for the specified GP"}, status=status.HTTP_404_NOT_FOUND)

    except GP.DoesNotExist:
        return Response({"detail": "GP not found"}, status=status.HTTP_404_NOT_FOUND)
    except Appointment.DoesNotExist:
        return Response({"detail": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def add_gp(request):
    """
    Add a new GP.
    """
    if request.method == 'POST':
        try:
            gp_name = request.data.get('name')
            slots_date_str = request.data.get('slots')
            description = request.data.get('description')

            if not gp_name or not slots_date_str:
                return Response({"detail": "GP name and slots date are required fields."}, status=status.HTTP_400_BAD_REQUEST)

            data = {
                "name": gp_name,
                "slots": datetime.strptime(slots_date_str, '%d/%m/%Y').date(),
                "description": description
            }

            # Create a new GP instance
            gp = GP(**data)
            gp.save()

            return Response({"detail": "GP added successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def update_gp(request, id):

    print("I AM HEREEE1")
    try:

        print("I AM HEREEE2")
        print("gp_id",request.data)
        gps = GP.objects.get(pk=id)
        print("gp_id",gps)
    except GP.DoesNotExist:
        return Response({'error': 'Enrollment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    print("I AM HEREEE")
    if request.method == 'POST':
        new_description = request.data.get('description')
        gps.description = new_description
        print("I AM HEREEE",new_description)
        gps.save()
        return Response({'message': 'Cart updated successfully'}, status=status.HTTP_200_OK)
        # serializer = GpSerializer(enrollment, data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewGP(RetrieveAPIView):
    queryset = GP.objects.all()
    serializer_class = GpSerializer
    lookup_field = 'id' 