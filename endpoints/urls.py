from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('populate/', views.PopulateLocationsView.as_view(), name='populate'),
    path('addlocation/', views.AddNewLocationView.as_view(), name = 'addlocation'),
    path('addfavourite/', views.AddFavouriteImageView.as_view(), name = 'addfavourite'),
    path('listfavourites/', views.GetFavouritePicturesView.as_view(), name = 'getfavourites'),
    path('search/', views.SearchLocationView.as_view(), name="search" ),
    path('locationsearch/', views.SavedLocationSearchView.as_view(),name = "locationsearch"),
    path('addnote/', views.AddNoteView.as_view(), name= "addnote"),
    path('listnotes/', views.GetNoteList.as_view(), name="listnote"),
    path('signup/', views.RegistrationView.as_view(), name="signup"),
    path('login/', obtain_auth_token),
    path('logout/', views.LogoutView.as_view()),
    path('userslist/', views.GetUsersList.as_view(), name = "userlist"),

]
