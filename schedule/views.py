from django.shortcuts import render
from django.utils import timezone
from .models import Location_weight, Station_info, State_info
import json
from django.http import HttpResponse

# Create your views here.
def schedule(request):
    # state_list = State_info.objects.all()
    return render(request, 'schedule/schedule.html', {'state_list' : state_li()})

def test_api(request):
    j = request.GET['key'][4:len(request.GET['key'])]
    result = []
    result.append({'type' : request.GET['key'][0:3]})

    for i in Location_weight.objects.filter(state = state_li()[j]):
        result.append({
            'location_name' : i.location,
        })

    return HttpResponse(json.dumps(result), content_type="application/json")

def state_li():
    result = {}
    for i in State_info.objects.all() :
        result[i.state_key] = i.state
    return result
