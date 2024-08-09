from rest_framework import serializers
from django.contrib.auth.models import User
import folium
import phonenumbers
from phonenumbers import geocoder
number="+25768497372"
class UserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user

class LocationSerializer(serializers.Serializer):
    location = serializers.CharField()
    service_provider = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
