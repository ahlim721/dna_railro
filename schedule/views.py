from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Location_weight, Station_info, State_info
from django.contrib.auth.models import User
from mypage.models import Travel_info
import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect

# Create your views here.
def schedule(request):
    # state_list = State_info.objects.all()
    return render(request, 'schedule/schedule.html', {'state_list' : state_li()})

def test_api(request):
    j = request.GET['key'][4:len(request.GET['key'])]
    result = []
    result.append(['type',request.GET['key'][0:3]])

    for i in Location_weight.objects.filter(state = state_li()[j]):
        result.append([
            i.loc_key,i.location
        ])

    return HttpResponse(json.dumps(result), content_type="application/json")

def state_li():
    result = {}
    for i in State_info.objects.all() :
        result[i.state_key] = i.state
    return result

def doschedule(request):
    # html에서 받아온 travel info 를 DB에 저장.
    sche = Travel_info (identifier = User.objects.get(username=request.user.get_username()),
                        railro_type = request.POST['railro_type'],
                        railro_day = request.POST['railro_day'],
                        start_loc = Location_weight.objects.get(loc_key=request.POST['start_loc']),
                        end_loc = Location_weight.objects.get(loc_key=request.POST['end_loc']),
                        start_date = request.POST['start_date'],
                        end_date = request.POST['end_date'],
                        )
    sche.save()
    # 방금 받았던 travel info의 기본키 값을 pk에 저장 후,
    pk = sche.travel_num
    # HttpResponseRedirect로 create뒤에 연결되게 format형식을 통해 create로 넘겨준다
    # 그렇게 되면 url은 -----/schedule/create/'해당travel_num'으로 만들어진다.
    return HttpResponseRedirect('create/{}'.format(pk))

def create(request, tnum):
    #생성된 pk를 tnum으로 받고, 그것을 쿼리셋을 통해 저장.
    sche = Travel_info.objects.get(travel_num = tnum)

    return render(request, 'schedule/create.html', {'sche' : sche})
