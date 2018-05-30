from django.shortcuts import render
import urllib.request
import json
from urllib.parse import quote
from schedule.models import Location_weight
from .models import Location_info,Location_festival
import ast
import datetime
from django.core import serializers
from django.http import HttpResponse




# 현재시간을 기준으로 url가져옴
current_day = datetime.datetime.now()
current_day = str(current_day)
current_day = current_day.replace("-","")
current_day = current_day.split(" ")
current_day = current_day[0]

# Create your views here.
'''
def makeFestival():
    check_city = ('서울', '인천', '대전', '대구', '광주', '부산', '울산', '세종특별자치시')

    num = 150
    url = "http://api.visitkorea.or.kr/openapi/service/rest/KorService/searchFestival?ServiceKey=At7nsk22aMwcKGFIVzySErarurTmPVDlxtfkUqF%2FGKDTtfWtNpvpFPZs8evW4Lkvf910SjBDwpxS2WMcB4JBlA%3D%3D&MobileOS=ETC&MobileApp=AppTest&numOfRows="+str(num)+"&arrange=P&eventStartDate="+current_day+"&_type=json"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    tmp = response.read().decode('utf8')

    jj = json.loads(tmp)

    for i in range(0,num):

        addr = jj["response"]["body"]["items"]["item"][i]["addr1"]
        pic = jj["response"]["body"]["items"]["item"][i]["firstimage"]
        sdate = jj["response"]["body"]["items"]["item"][i]["eventstartdate"]
        edate = jj["response"]["body"]["items"]["item"][i]["eventenddate"]

        title = jj["response"]["body"]["items"]["item"][i]["title"]

        city = addr
        flag = True

        # 특별시, 광역시, 특별자치시를 제외
        for j in check_city:
            cc = city.find(j)
            if cc!=-1:
                city = j
                flag = False
                break


        list = addr.split(" ")


        # 지역이름에 '시군구'가 들어있는 지역을 제외
        if flag!=False and list[1].find("군산") and list[1].find("군위") and list[1].find("구로") and list[1].find("구미") and list[1].find("대구"):
            flag = False
            tmp = list[1]
            city = tmp[0:len(list[1])-1]



        if flag is True:
            if list[1].find("시"):
                city = list[1].replace("시", "")
            elif (list[1].find("군")):
                city = list[1].replace("군", "")
            elif list[1].find("구"):
                city = list[1].replace("구", "")


        for j in Location_weight.objects.all():
            j = str(j)
            if city == j:
                Location_festival.objects.create(city = city,addr = addr, pic = pic, title= title, start_date = sdate, end_date= edate)
                break

'''
'''
def makeInfo():
    for i in Location_weight.objects.all():
        url = "http://api.visitkorea.or.kr/openapi/service/rest/KorService/searchKeyword?ServiceKey=At7nsk22aMwcKGFIVzySErarurTmPVDlxtfkUqF%2FGKDTtfWtNpvpFPZs8evW4Lkvf910SjBDwpxS2WMcB4JBlA%3D%3D&keyword=" + urllib.parse.quote(i.location) + "&MobileOS=ETC&MobileApp=AppTest&numOfRows=6&arrange=P&_type=json"
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        tmp = response.read().decode('utf8')

        jj = json.loads(tmp)
        city = i.location

        hello = jj["response"]["body"]["items"]["item"]
        jj_length = len(hello)

        for j in range(0,jj_length):
            print(city, " ", j)
            if not "addr1" in hello[j]:
                continue
            if not "firstimage" in hello[j]:
                continue
            if not "title" in hello[j]:
                continue
            addr= jj["response"]["body"]["items"]["item"][j]["addr1"]
            pic = jj["response"]["body"]["items"]["item"][j]["firstimage"]
            title = jj["response"]["body"]["items"]["item"][j]["title"]
            Location_info.objects.create(city = city,addr = addr, pic = pic, title= title)

'''
def searchLoc(request):
    loc = request.GET['loc']
    loc_list = []
    for i in Location_info.objects.filter(city = loc):
        li = {}
        li['pic'] = i.pic
        li['city'] = i.city
        li['title'] = i.title
        li['addr'] = i.addr
        loc_list.append(li)

    return HttpResponse(json.dumps(loc_list), content_type = 'application/json')

def location(request):
    #print("pic is "+pic+"city name is "+i+"address is"+addr+"title is "+title)
    #makeInfo()
    #makeFestival()



    loc = Location_info.objects.all()
    festival = Location_festival.objects.all()

    return render(request, 'location/location.html', {"loc" : loc, "festival" : festival})
