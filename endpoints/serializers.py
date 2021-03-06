from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers

from .models import FavouriteImage, Location, Note

class PopulateLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('location_name','id', 'user')
    
class AddNewLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('latitude', 'longitude', 'location_name', 'user')

class AddFavouriteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteImage
        fields = ('user','id','secret', 'farm', 'server','title')

class SearchLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('latitude', 'longitude')

class AddNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('user','image', 'text')
    
class ListFavouritesId(serializers.ModelSerializer):
    class Meta:
        model = FavouriteImage
        fields = ('id','user')

class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password',})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2',)
        extra_kwargs = {
            'password' : {'write_only' : True}
        }
    
    def save(self):
        user = User(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': "Passwords must match."})
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id')