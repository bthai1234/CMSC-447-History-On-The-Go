from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Itinerary(models.Model):
    """A user's saved itinerary of locations 

    Attributes:
        - id (PRIMARY KEY)
        - itinerary_name (NOT NULL)
        - locations (need another table for locations)
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True
    )
    itinerary_name = models.CharField(max_length=100)
    # location = models.ForeignKey()


class UserLocation(models.Model):
    """Stores a user's saved location

    Attributes:
        - id (PRIMARY KEY)
        - address (NOT NULL)
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    address = models.CharField(max_length=200)


class HistoricalLocation(models.Model):
    """Stores information regarding a historically relevant location

    Attributes:
        - id (PRIMARY KEY)
        - location_name (NOT NULL)
        - location_address (NOT NULL)
        - latitude (REAL UNIQUE NOT NULL)
        - longitude (REAL UNIQUE NOT NULL)
        - description (TEXT)
        - operation_hours (TIME)
        - pictures (BLOB)
    """
    loc_name = models.CharField(max_length=100)
    loc_address = models.CharField(max_length=200)
    latitude = models.DecimalField(unique=True)
    longitude = models.DecimalField(unique=True)
    description = models.TextField()
    operation_hours = models.TimeField()
    pictures = models.BinaryField() 