import os
import requests
import logging

from dotenv import load_dotenv
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
        permission_classes = [IsAuthenticated]
        queryset = Location.objects.all()
        serializer_class = PopulateLocationsSerializer

class AddNewLocationView(CreateAPIView):
        permission_classes = [IsAuthenticated]
        serializer_class = AddNewLocationSerializer

class AddFavouriteLocationView(CreateAPIView):
        permission_classes = [IsAuthenticated]
        serializer_class = AddFavouriteImageSerializer

class GetFavouritePicturesView(ListAPIView):
        permission_classes = [IsAuthenticated]
        # pagination_class = PageNumberPagination
        queryset = FavouriteImage.objects.all()
        serializer_class = AddFavouriteImageSerializer
        
class SearchLocationView(APIView):
        permission_classes = [IsAuthenticated]
        def get(self, request):
                try:
                        latitude = request.query_params['latitude']
                        longitude = request.query_params['longitude']
                        page = request.query_params['page']
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
        permission_classes = [IsAuthenticated]
        def get(self, request):
                location = request.query_params['location']
                page = request.query_params['page']
                flickr_url = FLICKR_API+location+"&per_page=9&page="+page+"&format=json&nojsoncallback=1"
                result = requests.get(flickr_url)
                data = result.json()
                return Response(data)

class AddNoteView(CreateAPIView):
        permission_classes = [IsAuthenticated]
        serializer_class = AddNoteSerializer

class GetNoteList(ListAPIView):
        permission_classes = [IsAuthenticated]
        serializer_class = AddNoteSerializer

        def get_queryset(self):
                id = self.request.query_params['id']
                # Note.objects.filter(image_id = id)
                res = Note.filter_by_id(self,id)
                data = AddNoteSerializer(res, many =True)
                print(data)
                return data.data

class RegistrationView(CreateAPIView):
        serializer_class = RegisterSerializer

        def post(self, request, *args, **kwargs):
                serializer = RegisterSerializer(data = request.data)
                data = {}
                if serializer.is_valid():
                        serializer.save()
                        data['response'] = "Registration Success"
                else:
                        data = serializer.errors
                return Response(data)
