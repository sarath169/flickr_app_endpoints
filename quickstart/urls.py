from django.urls import path
from knox import views as knox_views

from . import views

urlpatterns = [
    path('populate/', views.PopulateLocationsView.as_view(), name='populate'),
    path('addlocation/', views.AddNewLocationView.as_view(), name = 'addlocation'),
    path('addfavourite/', views.AddFavouriteLocationView.as_view(), name = 'addfavourite'),
    path('listfavourites/', views.GetFavouritePicturesView.as_view(), name = 'getfavourites'),
    path('search/', views.SearchLocationView.as_view(), name="search" ),
    path('locationsearch/', views.SavedLocationSearchView.as_view(),name = "locationsearch"),
    path('addnote/', views.AddNoteView.as_view(), name= "addnote"),
    path('listnotes/', views.GetNoteList.as_view(), name="listnote"),
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

]
