import os
import requests
import logging

from dotenv import load_dotenv
from django.shortcuts import render
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.serializers import AuthTokenSerializer

# Create your views here.
from .models import FavouriteImage, Location, Note
from .serializers import *

logger = logging.getLogger(__name__)
load_dotenv()

class PopulateLocationsView(ListAPIView):
        queryset = Location.objects.all()
        serializer_class = PopulateLocationsSerializer

class AddNewLocationView(CreateAPIView):
        serializer_class = AddNewLocationSerializer

class AddFavouriteLocationView(CreateAPIView):
        serializer_class = AddFavouriteImageSerializer

class GetFavouritePicturesView(ListAPIView):
        # pagination_class = PageNumberPagination
        # queryset = FavouriteLocations.objects.all()
        serializer_class = AddFavouriteImageSerializer
        def get_queryset(self):
                """
                This view should return a list of all the purchases
                for the currenttly authenticated user.
                """
                # location_name = self.request.location
                return FavouriteImage.objects.all()
        

class SearchLocationView(APIView):
        def get(self, request):
                latitude = request.query_params['latitude']
                longitude = request.query_params['longitude']
                page = request.query_params['page']
                openweather_url = "https://api.openweathermap.org/geo/1.0/reverse?lat="+latitude+"&lon="+longitude+"&limit=2&appid="+os.getenv('OPENWEATHERMAP_API_KEY')
                openweather_response = requests.get(openweather_url).json()
                print(openweather_response[0]['name'], "@@@@@@")
                location = openweather_response[0]['name']
                flickr_url = "https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key="+os.getenv('FLICKR_API_KEY')+"&text="+location+"&per_page=9&page="+page+"&format=json&nojsoncallback=1"
                r = requests.get(flickr_url)
                data = r.json()
                return Response(data)

class SavedLocationSearchView(APIView):
        def get(self, request):
                location = request.query_params['location']
                # locationid = Location.objects.values('id').get(location_name=location)['id']
                page = request.query_params['page']
                flickr_url = "https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key="+os.getenv('FLICKR_API_KEY')+"&text="+location+"&per_page=9&page="+page+"&format=json&nojsoncallback=1"
                r = requests.get(flickr_url)
                data = r.json()
                # data["id"] = locationid
                return Response(data)

class AddNoteView(CreateAPIView):
        serializer_class = AddNoteSerializer

class GetNoteList(ListAPIView):

        serializer_class = AddNoteSerializer
        def get_queryset(self):
                id = self.request.query_params['id']
                res = Note.objects.filter(image_id = id)
                data = AddNoteSerializer(res, many =True)
                print(data)
                return data.data
