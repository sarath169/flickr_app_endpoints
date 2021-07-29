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

