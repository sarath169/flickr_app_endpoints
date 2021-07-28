import requests
import logging

from django.shortcuts import render
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

# Create your views here.
from .models import FavouriteImage, Location, Note
from .serializers import *
logger = logging.getLogger(__name__)

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
                openweather_url = "https://api.openweathermap.org/geo/1.0/reverse?lat="+latitude+"&lon="+longitude+"&limit=2&appid=6e8191be847ff6c5327edad46cba4cdf"
                # opencage_url = "https://api.opencagedata.com/geocode/v1/json?key=fd47019dae064be5862063a4429fddd2&q="+latitude+"%2C"+longitude+"&pretty=1&no_annotations=1"
                openweather_response = requests.get(openweather_url).json()
                print(openweather_response[0]['name'], "@@@@@@")
                location = openweather_response[0]['name']
                # locationid = Location.objects.values('id').get(location_name=location)['id']
                # location = "chennai"
                # locationid = 1
                flickr_url = "https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key=f5e3dc5e6886a1e7799eeb85aad99cb5&text="+location+"&per_page=9&page="+page+"&format=json&nojsoncallback=1"
                r = requests.get(flickr_url)
                data = r.json()
                return Response(data)

class SavedLocationSearchView(APIView):
        def get(self, request):
                location = request.query_params['location']
                # locationid = Location.objects.values('id').get(location_name=location)['id']
                page = request.query_params['page']
                flickr_url = "https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key=f5e3dc5e6886a1e7799eeb85aad99cb5&text="+location+"&per_page=9&page="+page+"&format=json&nojsoncallback=1"
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
                
                return Note.objects.filter(image_id = id)

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)