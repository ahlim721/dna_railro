from django.db import models
from schedule.models import Location_weight

# Create your models here.
class Location_info(models.Model):
    recommend_place = models.TextField()
