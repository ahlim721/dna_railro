from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Location_weight, Station_info, State_info, Location_dist, Location_value, RailalTrue
from django.contrib.auth.models import User
from mypage.models import Travel_info, Travel_list
import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q
import math
import ast
import urllib.request
from urllib.parse import quote
import requests

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
        #Location_dist.objects.create(location = iw, dist = str(tmp))
        h = Location_dist.objects.get(location = iw)
        h.dist = str(tmp)
# 입력된 두 지역의 위도, 경도를 입력받아, 지역간의 거리를 int형식으로 반환.
'''
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
    # 초기에 지역사이의 루트를 저장하도록 한다.
    '''
    for i in Location_weight.objects.all():
        gettime = {}
        for j in Location_weight.objects.all():
            tmp = findRouteRail(i, j)
            if tmp:
                gettime[j.location] = tmp
            else:
                continue
        try:
            hhh = RailalTrue.objects.get(location = i)
            hhh.has_time = gettime
            hhh.save()
        except RailalTrue.DoesNotExist:
            RailalTrue.objects.create(location = i, has_time = gettime)
    '''
    '''
    for i in Location_weight.objects.all():
        if i.location == '용산':
            continue
        if i.location == '부산':
            continue
        gettime = {}
        for j in Location_weight.objects.all():
            tmp = findRouteRail(i, j)
            if tmp:
                gettime[j.location] = tmp
            else:
                continue
        try:
            hhh = RailalTrue.objects.get(location = i)
            hhh.has_time = gettime
            hhh.save()
        except RailalTrue.DoesNotExist:
            RailalTrue.objects.create(location = i, has_time = gettime)
    '''
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

    #go = RailalTrue.objects.get(location = start_loc).has_time

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

    cango = ast.literal_eval(RailalTrue.objects.get(location = start_loc).has_time)
    go_list = list(cango.keys())

    # 선택한 테마에 대해 내림차순으로 정렬 후, 5개로 자른다.
    Loc_list = list(set(pop_list)&set(thema_list)&set(close_list)&set(go_list))

    for i in Loc_list :
        pk = Location_weight.objects.get(location = i)
        result.append([
            pk.loc_key, i
        ])
    return HttpResponse(json.dumps(result), content_type="application/json")

def findRoute(request):
    tnum = Travel_info.objects.get(travel_num = request.GET['tnum'])
    lnum = request.GET['lnum']
    start_loc = Location_weight.objects.get(loc_key = request.GET['start_loc'])
    end_loc = Location_weight.objects.get(loc_key = request.GET['end_loc'])

    route = ast.literal_eval(RailalTrue.objects.get(location = start_loc.location).has_time)
    loc_route = route[end_loc.location]

    return HttpResponse(json.dumps(loc_route), content_type="application/json")

def saveTime(request):
    tnum = Travel_info.objects.get(travel_num = request.GET['tnum'])
    lnum = request.GET['lnum']
    end_loc = Location_weight.objects.get(loc_key = request.GET['end_loc'])
    start_date = request.GET['start_date']
    detail = request.GET['detail']

    if lnum == '1':
        start_loc = Location_weight.objects.get(location = tnum.start_loc)
    else:
        start_loc = Location_weight.objects.get(location = Travel_list.objects.filter(travel_num = tnum).get(leg_num = lnum-1).start)

    try:
        hhh = Travel_list.objects.filter(travel_num = tnum).get(leg_num = lnum)
        hhh.start_loc = start_loc
        hhh.end_loc = end_loc
        hhh.start_date = start_date
        hhh.detail = detail
        hhh.save()
    except Travel_list.DoesNotExist:
        Travel_list.objects.create(travel_num = tnum, leg_num = lnum, start=start_loc, end=end_loc, start_date = start_date, detail = detail)

    lnum = str(int(lnum)+1)

    return HttpResponse(json.dumps({'lnum' : lnum}), content_type="application/json")


'''
# start_st에서 end_st으로 갈 수 있는 경우의 시간표를 dictionary형태로 반환한다.
def getTimeTable(start_st, end_st, railType):
    try:
        info = Station_info.objects.get(station = start_st)
    except Station_info.DoesNotExist:
        return False
    try:
        h = Station_info.objects.get(station = end_st)
    except Station_info.DoesNotExist:
        return False
    TT = ast.literal_eval(info.timeTable)
    if not end_st in TT:
        return False
    sToe = ast.literal_eval(TT[end_st])
    timeTable=[]
    for i in sToe['station']:
        if railType == 'general':
            if "KTX" in i['trainClass']:
                continue
            if "SRT" in i['trainClass']:
                continue
        tmp = {}
        tmp['departureTime'] = int(i['departureTime'].replace(":",""))
        tmp['arrivalTime'] = int(i['arrivalTime'].replace(":",""))
        tmp['trainClass'] = i['trainClass']
        timeTable.append(tmp)
    return timeTable


# arrivalTime보다 arrivalTime의 시간표 중 늦고 가장 가까운 것을 반환하는 함수
def determine(arrivaltime, arrival_table):
    for i in arrival_table:
        if arrivaltime < i['departureTime']:
            return i
    return False

# korail을 크롤링하여, 출발역과 도착역 사이의 환승역이 있는지를 검사.
def findAtkorail(txtGoStart, txtGoEnd):
    params = {'txtGoStart' : txtGoStart, 'txtGoEnd' : txtGoEnd}
    url = "http://www.letskorail.com/ebizprd/sw_pr11311_i1Svt.do"
    r = requests.post(url, data = params)
    l = r.text
    if '잘못' in l:
        return False
    if '없습니다' in l:
        return False
    if 'tbody' in l:
        u = str(l.split('tbody')[1])
        u = u.replace('\t', '')
        u = u.replace('\r', '')
        u = u.replace('\n', '')
        b = u.split('</td><td>')[1:]
        result = []
        for i in range(int(len(b)/4)):
            result.append(b[i*4].split(' → ')[1])
        return result
    return False

# Google의 api를 받아와, 출발역과 도착역 사이의 최단 경로(역)을 반환.
def findAtGoogle(start_st, end_st, railType):
    url = "https://maps.googleapis.com/maps/api/directions/json?origin="+quote(start_st)+"&destination="+quote(end_st)+"&key=AIzaSyBkSK9z3yW-zfjFu0FCPlEqgaVVWGTtBT4&mode=transit&transit_mode=rail&language=ko"
    grequest = urllib.request.Request(url)
    gresponse = urllib.request.urlopen(grequest)
    route = ast.literal_eval(gresponse.read().decode('utf-8'))

    if not 'routes' in route:
        return []
    if not route['routes']:
        return []
    leg = route["routes"][0]["legs"]
    legs = []
    for i in leg:
        steps = []
        flag = True
        for j in i["steps"]:
            if("transit_details" in j):
                tmp = {}
                tmp["start_st"] = j["transit_details"]["departure_stop"]["name"]
                if tmp["start_st"] == '천안아산역 (온양온천)':
                    tmp["start_st"] == '천안아산역'
                tmp["end_st"] = j["transit_details"]["arrival_stop"]["name"]
                f = getTimeTable(tmp["start_st"],tmp["end_st"],railType)
                if not f:
                    flag = False
                    break
                tmp["timeTable"] = sorted(f, key=lambda k: k['arrivalTime'])
                steps.append(tmp)
        if flag:
            legs.append(steps)
    return legs


def makeStep(start_st, end_st, timeTable):
    step = {}
    step['start_st'] = start_st
    step['end_st'] = end_st
    step['timeTable'] = timeTable
    return step

def findRouteRail(start_loc, end_loc):
    # 출발, 도착 지역에 있는 기차역 중, main_station인 기차역을 가져온다.
    start_st = Station_info.objects.filter(location = start_loc.location).filter(main_station = True)
    end_st = Station_info.objects.filter(location = end_loc.location).filter(main_station = True)
    route = []

    for i in start_st:
        for j in end_st:
            step = []
            u = ast.literal_eval(i.timeTable)
            if j.station in u:
                print("직통 : " + str(i.station) + " 에서 " + str(j.station) + " 로")
                tmp = getTimeTable(i.station, j.station, 'general')
                step.append(makeStep(i.station, j.station, sorted(tmp, key=lambda k: k['arrivalTime'])))
                route.append(step)
            else:
                tmp = findAtkorail(i.station[:len(i.station)-1], j.station[:len(j.station)-1])
                if tmp:
                    print("코레일 : " + str(i.station) + " 에서 " + str(j.station) + " 로")
                    for u in tmp:
                        step = []
                        first = {}
                        second = {}
                        first['start_st'] = i.station
                        first['end_st'] = str(u)+'역'
                        f = getTimeTable(first['start_st'], first['end_st'], 'general')
                        if not f:
                            break
                        first['timeTable'] = sorted(f, key=lambda k: k['arrivalTime'])
                        step.append(first)
                        second['start_st'] = str(u)+'역'
                        second['end_st'] = j.station
                        f = getTimeTable(second['start_st'], second['end_st'], 'general')
                        if not f:
                            break
                        second['timeTable'] = sorted(f, key=lambda k: k['arrivalTime'])
                        step.append(second)
                        route.append(step)
                # 코레일에서 정보가 없을 경우, Google을 이용하여 검색
                else:
                    htt = findAtGoogle(i.station, j.station, 'general')
                    if htt:
                        print("구글 : " + str(i.station) + " 에서 " + str(j.station) + " 로")
                        route.extend(htt)

    result = []
    if not route:
        print("그런데도 없어요ㅠㅅㅠ " + str(end_st[0].station))
        return False
    for i in route:
        for j in i[0]["timeTable"]:
            start = j['arrivalTime']
            flag = True
            step = [makeStep(i[0]['start_st'], i[0]['end_st'], j)]
            for l in range(len(i)):
                if l == 0:
                    continue
                tmp = determine(start, i[l]['timeTable'])
                if not tmp:
                    flag = False
                    break
                step.append(makeStep(i[l]['start_st'], i[l]['end_st'], tmp))
                start = tmp['arrivalTime']
            if not flag:
                break
            result.append(step)
    return result
'''
