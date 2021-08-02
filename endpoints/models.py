from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    location_name = models.CharField(max_length=256)
    
    class Meta:
        db_table = "Locations"

class FavouriteImage(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    secret = models.CharField(max_length=256)
    farm = models.CharField(max_length=256)
    server = models.CharField(max_length =256)
    title = models.CharField(max_length=256, default="Default_Title")

    class Meta:
        db_table = "FavouriteImages"

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(FavouriteImage, on_delete=models.CASCADE)
    text = models.TextField()

    def filter_by_id(self,id, user):
        return Note.objects.filter(image_id = id, user_id= user)

    class Meta:
        db_table = "Notes"