from django.shortcuts import render
import urllib.request
import json
from urllib.parse import quote
from schedule.models import Location_weight
from .models import Location_info
import ast

# Create your views here.
'''
def useApi():
    city = {}
    for i in Location_weight.objects.all():
        url = "http://api.visitkorea.or.kr/openapi/service/rest/KorService/searchKeyword?ServiceKey=At7nsk22aMwcKGFIVzySErarurTmPVDlxtfkUqF%2FGKDTtfWtNpvpFPZs8evW4Lkvf910SjBDwpxS2WMcB4JBlA%3D%3D&keyword=" + urllib.parse.quote(i.location) + "&MobileOS=ETC&MobileApp=AppTest&numOfRows=1&arrange=P&_type=json"
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        tmp = response.read().decode('utf8')

        jj = json.loads(tmp)

        body = []
        item = {}

        item["addr"] = jj["response"]["body"]["items"]["item"]["addr1"]
        item["pic"] = jj["response"]["body"]["items"]["item"]["firstimage"]
        item["title"] = jj["response"]["body"]["items"]["item"]["title"]

        body.append(item)
        city[i.location] = body

    Location_info.objects.create(recommend_place = city)
'''

def location(request):
    #print("pic is "+pic+"city name is "+i+"address is"+addr+"title is "+title)
    '''useApi()'''
    i = Location_info.objects.get(id=1)
    rec = i.recommend_place
    hello = ast.literal_eval(rec)
    loc = Location_weight.objects.all()
    loc_name = []
    for i in loc:
        loc_name.append(i.location)
    return render(request, 'location/location.html', {"hello" : hello, "loc_name" : loc_name})
