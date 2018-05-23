from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Location_weight, Station_info, State_info, Location_dist, Location_value
from django.contrib.auth.models import User
from mypage.models import Travel_info
import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q
import math
import ast
import urllib.request
from urllib.parse import quote

# Create your views here.
# 각 지역간의 거리를 dictionary 형식으로 Location_dist 테이블에 저장.
'''
def make_Dist_List():
    for i in Location_value.objects.all():
        iw = Location_weight.objects.get(location = i.location)
        tmp = {}
        for j in Location_value.objects.all():
            jw = Location_weight.objects.get(location = j.location)
            tmp[jw.location] = cal_Dist(i.latitude, i.longtitude, j.latitude, j.longtitude)
        Location_dist.objects.create(location = iw, dist = str(tmp))
'''
# 입력된 두 지역의 위도, 경도를 입력받아, 지역간의 거리를 int형식으로 반환.
'''
def cal_Dist(lat1, lon1, lat2, lon2):
    R = 6373.0

    dlat1 = math.radians(lat1)
    dlon1 = math.radians(lon1)
    dlat2 = math.radians(lat2)
    dlon2 = math.radians(lon2)

    dlon = dlon2 - dlon1
    dlat = dlat2 - dlat1

    a = math.sin(dlat / 2)**2 + math.cos(dlat1) * math.cos(dlat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return int(R * c)
'''
'''
def make_TimeTable():
    i = Station_info.objects.get(station = '희방사역')
    timeTable = {}
    for j in Station_info.objects.all():
        if i==j:
            continue
        url = "https://api.odsay.com/v1/api/trainServiceTime?lang=0&startStationID="+str(int(i.stationID))+"&endStationID="+str(int(j.stationID))+"&apiKey=WcSrakZHikdXHeqm/pUetMaMRiS1iVq%2blMWrWeSG0Q8"
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        tmp = ast.literal_eval(response.read().decode('utf-8'))
        if not tmp:
            continue;
        else:
            timeTable[j.station] = str(tmp['result'])
    i.timeTable = timeTable
    i.save()
'''
'''
def get_stationID():
    for i in Station_info.objects.all():
        sta = i.station[:len(i.station)-1]
        url = "https://api.odsay.com/v1/api/searchStation?lang=0&stationName="+quote(sta)+"&stationClass=3&apiKey=WcSrakZHikdXHeqm/pUetMaMRiS1iVq%2blMWrWeSG0Q8"
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        ID = ast.literal_eval(response.read().decode('utf-8'))['result']['station'][0]['stationID']
        i.stationID = ID
        i.save()
'''

def schedule(request):
    # state_list = State_info.objects.all()
    # 초기에 각 지역간의 거리를 테이블로 저장하기 위해 함수를 실행시킨 후 주석 처리함.
    '''make_Dist_List()'''
    # 초기에 api 사용을 위하여 각 기차역의 고유 번호인 stationID를 받아 저장한 후 주석 처리함.
    '''get_stationID()'''
    # 초기에 api를 활용하여 각 기차역에서의 시간표를 저장하도록 한다.
    '''make_TimeTable()'''
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
    st_l = Location_weight.objects.get(location = sche.start_loc)
    en_l = Location_weight.objects.get(location = sche.end_loc)

    return render(request, 'schedule/create.html', {'sche' : sche, 'st_l' : st_l, 'en_l' : en_l})

def findThema(request):
    thema = "-" + request.GET['key']
    start_loc = Location_weight.objects.get(loc_key = request.GET['start_loc'])
    end_loc = Location_weight.objects.get(loc_key = request.GET['end_loc'])
    num_of_list = int(Location_weight.objects.count()/2)

    result = []
    pop_list = []
    thema_list = []

    pop = Location_weight.objects.order_by('-popular')#[:num_of_list]
    for i in pop:
        pop_list.append(i.location)

    thema = Location_weight.objects.order_by(thema)[:num_of_list]
    for i in thema:
        thema_list.append(i.location)

    tmmp = Location_dist.objects.get(location = start_loc)
    close_list = ast.literal_eval(tmmp.dist)
    close_list = sorted(close_list, key=lambda k : close_list[k], reverse=True)
    close_list = close_list[:num_of_list]

    # 선택한 테마에 대해 내림차순으로 정렬 후, 5개로 자른다.
    Loc_list = list(set(pop_list)&set(thema_list)&set(close_list))

    for i in Loc_list :
        pk = Location_weight.objects.get(location = i)
        result.append([
            pk.loc_key, i
        ])
    return HttpResponse(json.dumps(result), content_type="application/json")

def findRoute(request):
    lnum = request.GET['lnum']
    start_loc = Location_weight.objects.get(loc_key = request.GET['start_loc'])
    end_loc = Location_weight.objects.get(loc_key = request.GET['end_loc'])

    url = "https://maps.googleapis.com/maps/api/directions/json?origin="+quote(start_loc.location)+"&destination="+quote(start_loc.location)+"&key=AIzaSyCx5i4WHK3_vn23BDHnaNqhc9bxMP2A83M&mode=transit&transit_mode=rail"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    route = ast.literal_eval(response.read().decode('utf-8'))

    leg = route['routes'][0]['legs']

    steps = []
    for i in leg:
        for j in i["steps"]:
            if("transit_details" in j):
                tmp = {}
                tmp["start_st"] = j["transit_details"]["departure_stop"]["name"]
                tmp["end_st"] = j["transit_details"]["arrival_stop"]["name"]
                steps.append(tmp)

    return HttpResponse(json.dumps(result), content_type="application/json")
