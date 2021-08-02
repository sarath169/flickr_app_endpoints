import os
import requests
import logging

from dotenv import load_dotenv
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView     


# Create your views here.
from .models import FavouriteImage, Location, Note
from .serializers import *
from flickr_app.settings import FLICKR_API

logger = logging.getLogger(__name__)
load_dotenv()

class PopulateLocationsView(ListAPIView):
        # This view populates the locations dropdown
        permission_classes = [IsAuthenticated]
        queryset = Location.objects.all()
        serializer_class = PopulateLocationsSerializer

class AddNewLocationView(CreateAPIView):
        # This view is to add new locations to database
        permission_classes = [IsAuthenticated]
        serializer_class = AddNewLocationSerializer
        def post(self, request):
                try:
                        print("fgwilewideiuwkcm")
                        # user = self.request.query_params['user']
                        # print(user)
                        serializer = AddNewLocationSerializer(data = self.request.data)

                        data = {}
                        if serializer.is_valid():
                                serializer.save()
                                data['response'] = "Registration Success"
                        else:
                                data = serializer.errors
                        return Response(data)
                except:
                        message = {"message" : "please provide all necessary values" }
                        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class AddFavouriteImageView(CreateAPIView):
        # This view is to add new image to favourites
        permission_classes = [IsAuthenticated]
        serializer_class = AddFavouriteImageSerializer

class GetFavouritePicturesView(ListAPIView):
        # This view is to list all the favourite images
        permission_classes = [IsAuthenticated]
        serializer_class = AddFavouriteImageSerializer
        def get_queryset(self):
                try:
                        user = self.request.query_params['user']
                        # Note.objects.filter(image_id = id)
                        print(user, "*********************")
                        result = FavouriteImage.objects.filter(user = user)
                        print(result)
                        return result
                except:
                        data = {"params":"please check the input parameters"}
                        return Response(data, status = status.HTTP_400_BAD_REQUEST)
        
class SearchLocationView(APIView):
        # This view is to get images for given latitude and longitude
        permission_classes = [IsAuthenticated]
        def get(self, request):
                try:
                        latitude = request.query_params['latitude']
                        longitude = request.query_params['longitude']
                        page = request.query_params['page']
                        # openweather api is used to get the location from given latitude and longitude
                        openweather_url = "https://api.openweathermap.org/geo/1.0/reverse?lat="+latitude+"&lon="+longitude+"&limit=2&appid="+os.getenv('OPENWEATHERMAP_API_KEY')
                        openweather_response = requests.get(openweather_url).json()
                        location = openweather_response[0]['name']
                        flickr_url = FLICKR_API+location+"&per_page=9&page="+page+"&format=json&nojsoncallback=1"
                        result = requests.get(flickr_url)
                        data = result.json()
                        return Response(data, status=status.HTTP_200_OK)
                except:
                        data = {"params":"please check the input parameters"}
                        return Response(data, status = status.HTTP_400_BAD_REQUEST)

class SavedLocationSearchView(APIView):
        # This view is to get images for saved locations
        permission_classes = [IsAuthenticated]
        def get(self, request):
                try:
                        location = request.query_params['location']
                        page = request.query_params['page']
                        flickr_url = FLICKR_API+location+"&per_page=9&page="+page+"&format=json&nojsoncallback=1"
                        result = requests.get(flickr_url)
                        data = result.json()
                        return Response(data)
                except:
                        data = {"params":"please check the input parameters"}
                        return Response(data, status = status.HTTP_400_BAD_REQUEST)

class AddNoteView(CreateAPIView):
        # This view is to add note to image
        permission_classes = [IsAuthenticated]
        def post(self, request):
                try:
                        print("*********************************************")
                        # user = self.request.query_params['user']
                        # print(user)
                        print(request.data)
                        serializer = AddNoteSerializer(data = self.request.data)

                        data = {}
                        if serializer.is_valid():
                                serializer.save()
                                data['response'] = "Registration Success"
                        else:
                                data = serializer.errors
                        return Response(data)
                except:
                        message = {"message" : "please provide all necessary values" }
                        return Response(message, status=status.HTTP_400_BAD_REQUEST)

class GetNoteList(ListAPIView):
        # This view is to get all the notes of the image
        permission_classes = [IsAuthenticated]
        serializer_class = AddNoteSerializer

        def get_queryset(self):
                try:
                        id = self.request.query_params['id']
                        user = self.request.query_params['user']
                        # Note.objects.filter(image_id = id)
                        print(id,user, "*********************88")
                        result = Note.filter_by_id(self,id, user)
                        print(result)
                        return result
                except:
                        data = {"params":"please check the input parameters"}
                        return Response(data, status = status.HTTP_400_BAD_REQUEST)

class RegistrationView(CreateAPIView):
        # This view is to register new users
        serializer_class = RegisterSerializer

        def post(self, request, *args, **kwargs):
                try:
                        serializer = RegisterSerializer(data = request.data)
                        data = {}
                        if serializer.is_valid():
                                serializer.save()
                                data['response'] = "Registration Success"
                        else:
                                data = serializer.errors
                        return Response(data)
                except:
                        message = {"message" : "please provide all necessary values" }
                        return Response(message, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
        # This view is to logout uers
        def get(self, request, format=None):
                try:
                        # simply delete the token to force a login
                        request.user.auth_token.delete()
                        data = {"message":"logout success"}
                        return Response(data, status=status.HTTP_200_OK)
                except:
                        message = {"message" : "Token not found" }
                        return Response(message, status=status.HTTP_404_NOT_FOUND)
                
class GetUsersList(ListAPIView):
        serializer_class = UserSerializer
        queryset = User.objects.all()