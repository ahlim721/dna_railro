from django.contrib import admin
from .models import Location_weight, Station_info, State_info
# Register your models here.

admin.site.register(Location_weight)
admin.site.register(State_info)
admin.site.register(Station_info)
