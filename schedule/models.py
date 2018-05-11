from django.db import models

# Create your models here.
class Location_weight(models.Model):
    loc_key = models.CharField(max_length=20)
    state = models.ForeignKey(
        'State_info',
        on_delete=models.CASCADE,
    )
    location = models.CharField(max_length=15, primary_key = True, null = False)
    eat = models.FloatField(default = 0)
    picture = models.FloatField(default = 0)
    activity = models.FloatField(default = 0)
    media = models.FloatField(default = 0)
    popular = models.FloatField(default = 0)

    def __str__(self):
        return self.location

class Station_info(models.Model):
    station_key = models.CharField(max_length=20)
    station = models.CharField(max_length=15, primary_key = True)
    location = models.ForeignKey(
        'Location_weight',
        on_delete=models.CASCADE,
    )
    KTX = models.BooleanField(default = False)
    ITX_C = models.BooleanField(default = False)
    ITX_S = models.BooleanField(default = False)
    S = models.BooleanField(default = False)
    M = models.BooleanField(default = False)
    N = models.BooleanField(default = False)
    Com = models.BooleanField(default = False)
    Tour = models.BooleanField(default = False)

    def __str__(self):
        return self.station

class State_info(models.Model):
    state_key = models.CharField(max_length=20, null = False)
    state = models.CharField(max_length=15, primary_key=True, null = False)

    def __str__(self):
        return self.state
