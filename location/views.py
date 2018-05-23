from django.shortcuts import render
import urllib.request
import json
from urllib.parse import quote
from schedule.models import Location_weight

tag_city = ['가평', '강릉', '경산', '경주', '계룡', '고양', '곡성', '공주', '광명', '광양', '광주', '구로', '구미', '군산', '군위', '김제', '김천', '김해'
            , '나주', '남양주', '남원', '논산'
            , '단양', '대구', '대전', '동대문', '동두천', '동작', '동해'
            , '목포', '무안', '문경', '밀양', '보령', '보성', '봉화', '부산'
            , '사천', '삼척', '상주', '서천', '성동', '세종', '수원', '순천'
            , '아산', '안동', '안양', '양산', '양평', '여수', '연천', '영덕', '영동', '영등포', '영월', '영주', '영천', '예산', '예천', '오산', '옥천',
            '완주'
            , '용산', '울산', '원주', '음성', '의성', '의정부', '익산', '임실'
            , '장성', '전주', '정선', '정읍', '제천', '중랑', '증평', '진주'
            , '창원', '천안', '철원', '청도', '청주', '춘천', '충주', '칠곡'
            , '태백'
            , '파주', '평창', '평택', '포항'
            , '하동', '함안', '함평', '홍성', '화순', '횡성']

# Create your views here.
def useApi():
    city = {}
    for i in tag_city:
        url = "http://api.visitkorea.or.kr/openapi/service/rest/KorService/searchKeyword?ServiceKey=At7nsk22aMwcKGFIVzySErarurTmPVDlxtfkUqF%2FGKDTtfWtNpvpFPZs8evW4Lkvf910SjBDwpxS2WMcB4JBlA%3D%3D&keyword=" + urllib.parse.quote(i) + "&MobileOS=ETC&MobileApp=AppTest&numOfRows=1&arrange=P&_type=json"
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

        city[i] = body




def location(request):
    
    #print("pic is "+pic+"city name is "+i+"address is"+addr+"title is "+title)


    return render(request, 'location/location.html', {})
