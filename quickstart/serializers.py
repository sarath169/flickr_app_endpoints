from django.contrib.auth.models import User
from rest_framework import serializers

from .models import FavouriteImage, Location, Note

class PopulateLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('location_name','id')
    
class AddNewLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('latitude', 'longitude', 'location_name')

class AddFavouriteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteImage
        fields = ('id','secret', 'farm', 'server','title')

class SearchLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('latitude', 'longitude')

class AddNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('image_id', 'text')
    
class ListFavouritesId(serializers.ModelSerializer):
    class Meta:
        model = FavouriteImage
        fields = ('id',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user