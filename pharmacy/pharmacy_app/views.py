from psycopg2 import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Medicines, Cart
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import api_view
from rest_framework.views import APIView

@api_view(['GET'])
def get_all_medicines(request):
    try:
        medicines = Medicines.get_all_medicines()

        # Serialize the medicines to JSON
        serialized_medicines = [{"id": medicine.id, "name": medicine.name, "description": medicine.description, "price": medicine.price} for medicine in medicines]

        return Response(serialized_medicines, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_medicine_details(request, medicine_id):
    """
    Get details of a specific medicine by its ID.
    """
    try:
        medicine = Medicines.objects.get(pk=medicine_id)
        medicine_data = {
            "id": medicine.id,
            "name": medicine.name,
            "description": medicine.description,
            "price": medicine.price,
            # Add other fields as needed
        }
        return Response(medicine_data, status=status.HTTP_200_OK)

    except Medicines.DoesNotExist:
        return Response({"detail": f"Medicine with ID {medicine_id} not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def add_medicine(request):
    if request.method == 'POST':
        try:
            medicine_name = request.data.get('name')
            description = request.data.get('description')
            price = request.data.get('price')

            if not medicine_name or not price:
                return Response({"detail": "Medicine name and price are required fields."}, status=status.HTTP_400_BAD_REQUEST)

            medicine = Medicines(name=medicine_name, description=description, price=price)
            medicine.save()

            return Response({"detail": "Medicine added successfully."}, status=status.HTTP_201_CREATED)

        except IntegrityError:
            # If a unique constraint violation occurs, retry with a new ID
            medicine.id = None
            medicine.save()

            return Response({"detail": "Medicine added successfully with a new ID."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def add_to_cart(request):
    if request.method == 'POST':
        cart_id = request.data.get('cart_id')
        medicine_id = request.data.get('medicine_id')

        if not cart_id or not medicine_id:
            return Response({'error': 'Both cart_id and medicine_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Call the method to add medicine to the cart
        cart, created = Cart.objects.get_or_create(cart_id=cart_id)
        result = Cart.add_medicine_to_cart(cart_id, medicine_id)

        if result:
            return Response({'message': 'Medicine added to the cart successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to add medicine to the cart.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def view_cart(request, cart_id):
    try:
        cart, created = Cart.objects.get_or_create(cart_id=cart_id)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        medicine_ids = cart.medicine_ids
        return Response({'medicine_ids': medicine_ids}, status=status.HTTP_200_OK)
    
@api_view(['PUT'])
def update_cart(request, cart_id):
    try:
        cart, created = Cart.objects.get_or_create(cart_id=cart_id)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        new_medicine_ids = request.data.get('medicine_ids', [])
        cart.medicine_ids = new_medicine_ids
        cart.save()
        return Response({'message': 'Cart updated successfully'}, status=status.HTTP_200_OK)
    
class GetCart(APIView):
    def get(self, request, cart_id):
        try:
            cart, created = Cart.objects.get_or_create(cart_id=cart_id)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get the list of medicine IDs in the cart
        medicine_ids = cart.medicine_ids

        # Retrieve medicine details for the medicine IDs
        medicines = Medicines.objects.filter(id__in=medicine_ids).values('id', 'name', 'description', 'price')

        return Response({'medicines': list(medicines)}, status=status.HTTP_200_OK)