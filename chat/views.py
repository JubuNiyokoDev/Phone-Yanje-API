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
import logging
from urllib.parse import unquote
from twilio.rest import Client

logger = logging.getLogger(__name__)

# Twilio credentials
TWILIO_ACCOUNT_SID = 'ACed48c7be790ea82f5a62708dc615d349'
TWILIO_AUTH_TOKEN = '146cc9765070143502ce38948a0af683'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

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

class FindLocationAPIByNumberView(APIView):
    def get(self, request, *args, **kwargs):
        phone_number = request.query_params.get('number')
        if not phone_number:
            logger.error("Phone number is missing")
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Nettoyage du numéro de téléphone
            phone_number = unquote(phone_number)
            phone_number = ''.join(filter(lambda x: x.isdigit() or x == '+', phone_number))  # Garde les chiffres et le +

            # Ajouter le préfixe +257 pour le Burundi si absent
            if not phone_number.startswith("+257"):
                phone_number = f"+257{phone_number}"

            logger.info(f"Processing phone number: {phone_number}")

            # Vérifier la validité du numéro de téléphone avec Twilio
            phone_info = client.lookups.v1.phone_numbers(phone_number).fetch(type=['carrier'])
            if not phone_info:
                logger.error(f"Invalid phone number: {phone_number}")
                return Response({'error': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)

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
                logger.error(f"Geocoding result not found for location: {location_description}")
                return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

            # Vérifier si les coordonnées sont uniques
            lat = result[0]['geometry']['lat']
            lng = result[0]['geometry']['lng']
            logger.info(f"Geocoding result: Latitude: {lat}, Longitude: {lng}")

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
            logger.error(f"Invalid phone number: {phone_number}")
            return Response({'error': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Exception occurred: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FindLocationAPIByEMEIView(APIView):
    def post(self, request, *args, **kwargs):
        return Response({'message': 'Comming Soon'}, status=401)
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Comming Soon'}, status=401)

class FindLocationAPIByGoogleView(APIView):
    def post(self, request, *args, **kwargs):
        return Response({'message': 'Comming Soon'}, status=401)
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Comming Soon'}, status=401)
