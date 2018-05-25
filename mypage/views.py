from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def user_update(request):
    return render(request, 'mypage/user_update.html', {} )
