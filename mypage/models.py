from django.db import models
from django.conf import settings
from schedule.models import Location_weight

# Create your models here.
class User_info(models.Model):
    identifier = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        #related_name = "username",
        on_delete=models.CASCADE,
        null=False,
        primary_key=True,
    )
    name = models.CharField(max_length=20, default = '')
    Loc_per = models.BooleanField(null=False, default = False)

    def __str__(self):
        return self.identifier

class Travel_info(models.Model):
    RAILRO_TYPES = (('general', 'general'), ('premium', 'premium'))
    RAILRO_DAYS = (('five', '5'), ('seven', '7'))
    identifier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        #related_name = "username",
        on_delete=models.CASCADE,
        null=False,
    )
    travel_num = models.AutoField(primary_key=True)
    railro_type = models.CharField(null=False, max_length=10, choices=RAILRO_TYPES, default='general')
    railro_day = models.CharField(null=False, max_length=10, choices=RAILRO_DAYS, default='five')
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    start_loc = models.ForeignKey(
        'schedule.Location_weight',
        related_name = "start_location",
    )
    end_loc = models.ForeignKey(
        'schedule.Location_weight',
        related_name = "end_location",
    )
    is_done = models.BooleanField(default = False)

class Travel_list(models.Model):
    travel_num = models.ForeignKey(
        'Travel_info',
        on_delete = models.CASCADE,
        null=False,
    )
    leg_num = models.FloatField(null=False)
    start = models.ForeignKey(
        'schedule.Location_weight',
        related_name = "start_loc",
        null=False
    )
    end = models.ForeignKey(
        'schedule.Location_weight',
        related_name = "end_loc",
        null=False
    )
    start_date = models.DateField(null=False)
    detail = models.CharField(null=False, max_length=250, default='')
