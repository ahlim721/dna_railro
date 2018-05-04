from django.db import models
from schedule.models import Location_weight

# Create your models here.
class User_info(models.Model):
    identifier = models.CharField(max_length=10, null=False, primary_key = True, default = '')
    password = models.CharField(max_length=10, null=False, default = '')
    name = models.CharField(max_length=5, default = '')
    Loc_per = models.BooleanField(null=False, default = False)

    def __str__(self):
        return self.identifier

class Travel_info(models.Model):
    RAILRO_TYPES = (('general', 'general'), ('premium', 'premium'))
    RAILRO_DAYS = (('five', '5'), ('seven', '7'))
    identifier = models.ForeignKey(
        'User_info',
        on_delete=models.CASCADE,
        default = '',
        primary_key = True,
    )
    travel_num = models.FloatField(primary_key = True, default = 0)
    railro_type = models.CharField(null=False, max_length=10, choices=RAILRO_TYPES, default='general')
    railro_day = models.CharField(null=False, max_length=10, choices=RAILRO_DAYS, default='five')
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    start_loc = models.ForeignKey(
        'schedule.Location_weight',
        related_name = "start_location",
        default = '',
    )
    end_loc = models.ForeignKey(
        'schedule.Location_weight',
        related_name = "end_location",
        default = '',
    )
    Travel_list = models.CharField(max_length=100, default = '')
    is_done = models.BooleanField(default = False)

    def __str__(self):
        return self.Travel_list
