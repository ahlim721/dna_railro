from django.db import models
from schedule.models import Location_weight

# Create your models here.
class Location_info(models.Model):
    city = models.CharField(max_length=50, null=False)
    addr = models.CharField(max_length=100)
    pic = models.CharField(max_length=400)
    title = models.CharField(max_length=100)


class Location_festival(models.Model):
    city = models.CharField(max_length=50, null=False)
    addr = models.CharField(max_length=100)
    pic = models.CharField(max_length=400)
    title = models.CharField(max_length=100)
    start_date = models.CharField(max_length=10)
    end_date = models.CharField(max_length=10)
