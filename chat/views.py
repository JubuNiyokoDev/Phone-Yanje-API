from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import LocationSerializer, UserCreationSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
from urllib.parse import unquote
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreationSerializer

class LoginUserView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
        else:
            return Response({'message': 'Invalid credentials'}, status=401)


import logging

logger = logging.getLogger(__name__)

class FindLocationAPIView(APIView):
    def get(self, request, *args, **kwargs):
        phone_number = request.query_params.get('number')
        if not phone_number:
            logger.error("Phone number is missing")
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            phone_number = unquote(phone_number)
            print(phone_number)
            # Parse the phone number
            # phone_number = '+25768497372'
            parsed_number = phonenumbers.parse(phone_number)
            location_description = geocoder.description_for_number(parsed_number, 'fr')
            service_provider = carrier.name_for_number(parsed_number, 'fr')

            if not location_description:
                logger.error("Location description not found")
                return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

            # Geocoding
            key = 'f808c7779f8948d18896a99cc53dd3cb'
            geocodeur = OpenCageGeocode(key)
            result = geocodeur.geocode(location_description)
            if not result:
                logger.error("Geocoding result not found")
                return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

            lat = result[0]['geometry']['lat']
            lng = result[0]['geometry']['lng']

            # Serialize the response
            serializer = LocationSerializer(data={
                'location': location_description,
                'service_provider': service_provider,
                'latitude': lat,
                'longitude': lng
            })
            serializer.is_valid(raise_exception=True)
            
            return Response(serializer.validated_data)

        except phonenumbers.NumberParseException:
            logger.error("Invalid phone number")
            return Response({'error': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Exception occurred: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
