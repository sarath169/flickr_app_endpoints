from django.db import models

# Create your models here.
class Location(models.Model):
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    location_name = models.CharField(max_length=256)

    class Meta:
        db_table = "Locations"

class FavouriteImage(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    secret = models.CharField(max_length=256)
    farm = models.CharField(max_length=256)
    server = models.CharField(max_length =256)
    title = models.CharField(max_length=256, default="Default_Title")

    class Meta:
        db_table = "FavouriteImages"

class Note(models.Model):
    text = models.TextField()
    image_id = models.ForeignKey(FavouriteImage, on_delete=models.CASCADE)

    def filter_by_id(self,id):
        return Note.objects.filter(id = id)

    class Meta:
        db_table = "Notes"