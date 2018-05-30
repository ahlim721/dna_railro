from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LeaveForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .models import Travel_info

# Create your views here.

@login_required
def user_leave(request):
    if request.method == "POST":
        form = LeaveForm(request.POST)
        username = request.user.get_username()
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            user.delete()
            return redirect('/')
        else:
            return HttpResponse('비밀번호가 틀렸습니다. 다시 시도 해보세요.')
    else:
        form = LeaveForm()
        return render(request, 'mypage/user_leave.html', {'form' : form} )

@login_required
def user_travellist(request):
    get_travel = Travel_info.objects.filter(identifier = User.objects.get(username = request.user.get_username()))
    li = []
    for i in get_travel:
        li.append(i)
    return render(request, 'mypage/user_travellist.html', {'Travel_list' : li})

def selectList(request):
    get_travel = Travel_list.objects.filter(travel_num = request.GET['key'])
    li =[]
    for i in get_travel:
        li.append(i)
    return HttpResponse(json.dumps(li), content_type = "application/json")
