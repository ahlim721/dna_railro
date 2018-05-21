from django.shortcuts import render
from django.utils import timezone
from .models import Board
from .models import Comment
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
rowsPerPage = 10

# Create your views here.

@login_required
def community(request):
    boardList = Board.objects.order_by('-id')[0:10]
    current_page =1

    # model 을 사용해서 전체 데이터 갯수를 구한다.
    totalCnt = Board.objects.all().count()

    # 이것은 페이징 처리를 위해 생성한 간단한 헬퍼 클래스이다. 별로 중요하지 않으므로 소스를 참조하기 바란다.
    pagingHelperIns = pagingHelper();
    totalPageList = pagingHelperIns.getTotalPageList( totalCnt, rowsPerPage)
    print ('totalPageList', totalPageList)

    # 템플릿으로 필요한 정보들을 넘기는 부분이다. 이를 통해서 정적인 템플릿에 동적인 데이터가 결합되게 되는 것이다.
    # 우리는 게시판 최초 화면 처리를 위해서 listSpecificPage.html 템플릿을 호출했다.
    # 그리고 필요한 정보들을 dictionary 로 전달했다.
    return render(request, 'community/community.html', {'boardList': boardList, 'totalCnt': totalCnt, 'current_page':current_page ,'totalPageList':totalPageList} )
class pagingHelper:
    "paging helper class"
    def getTotalPageList(self, total_cnt, rowsPerPage):
        if ((total_cnt % rowsPerPage) == 0):
            self.total_pages = total_cnt / rowsPerPage;
            #print 'getTotalPage #1'
        else:
            self.total_pages = (total_cnt / rowsPerPage) + 1;
            #print 'getTotalPage #2'

        self.totalPageList = []
        for j in range( int(self.total_pages) ):
            self.totalPageList.append(j+1)

        return self.totalPageList

    def __init__(self ):
        self.total_pages = 0
        self.totalPageList  = 0

def show_write_form(request):
    return render(request, 'community/writeBoard.html')

@csrf_exempt
def DoWriteBoard(request):
    br = Board (subject = request.POST['subject'],
                      name = User.objects.get(username=request.user.get_username()),
                      memo = request.POST['memo'],
                      created_date = timezone.now(),
                      hits = 0
                     )
    br.save()

    # 다시 조회
    url = '/community?current_page=1'
    return HttpResponseRedirect(url)

def viewWork(request):
    pk= request.GET['memo_id']
    #print 'pk='+ pk
    boardData = Board.objects.get(id=pk)
    #print boardData.memo

    commentData = Comment.objects.all()


    # Update DataBase
    #print 'boardData.hits', boardData.hits
    Board.objects.filter(id=pk).update(hits = boardData.hits + 1)

    return render(request, 'community/viewMemo.html', {'memo_id': request.GET['memo_id'],
                                                'current_page':request.GET['current_page'],
                                                'searchStr': request.GET['searchStr'],
                                                'boardData': boardData , 'commentData':commentData  } )

def viewForUpdate(request):
    memo_id = request.GET['memo_id']
    current_page = request.GET['current_page']
    searchStr = request.GET['searchStr']

    #totalCnt = DjangoBoard.objects.all().count()
    #print 'memo_id', memo_id
    #print 'current_page', current_page
    #print 'searchStr', searchStr

    boardData = Board.objects.get(id)

    return render(request, 'community/viewForUpdate.html', {'memo_id': request.GET['memo_id'],
                                                'current_page':request.GET['current_page'],
                                                'searchStr': request.GET['searchStr'],
                                                'boardData': boardData } )


@csrf_exempt
def updateBoard(request):
    memo_id = request.POST['memo_id']
    current_page = request.POST['current_page']
    searchStr = request.POST['searchStr']

    #print '#### updateBoard ######'
    #print 'memo_id', memo_id
    #print 'current_page', current_page
    #print 'searchStr', searchStr

    # Update DataBase
    Board.objects.filter(id=memo_id).update(
                                                  subject= request.POST['subject'],
                                                  memo= request.POST['memo']
                                                  )

    # Display Page => POST 요청은 redirection!
    url = '/community?current_page=' + str(current_page)
    return HttpResponseRedirect(url)


def viewForDelete(request):
    memo_id = request.GET['memo_id']
    current_page = request.GET['current_page']
    #print '#### DeleteSpecificRow ######'
    #print 'memo_id', memo_id
    #print 'current_page', current_page

    p = Board.objects.get(id=memo_id)
    p.delete()

    # Display Page
    # 마지막 메모를 삭제하는 경우, 페이지를 하나 줄임.
    totalCnt = Board.objects.all().count()
    pagingHelperIns = pagingHelper();

    totalPageList = pagingHelperIns.getTotalPageList( totalCnt, rowsPerPage)
    #print 'totalPages', totalPageList

    if( int(current_page) in totalPageList):
        #print 'current_page No Change'
        current_page=current_page
    else:
        current_page= int(current_page)-1
        #print 'current_page--'

    url = '/community?current_page=' + str(current_page)
    return HttpResponseRedirect(url)

@csrf_exempt
def searchWithSubject(request):
    searchStr = request.POST['searchStr']
    #print 'searchStr', searchStr

    url = 'listSearchedSpecificPageWork?searchStr=' + searchStr +'&pageForView=1'
    return HttpResponseRedirect(url)


def listSearchedSpecificPageWork(request):
    searchStr = request.GET['searchStr']
    pageForView = request.GET['pageForView']
    #print 'listSearchedSpecificPageWork:searchStr', searchStr, 'pageForView=', pageForView

    #boardList = DjangoBoard.objects.filter(subject__contains=searchStr)
    #print  'boardList=',boardList

    totalCnt = Board.objects.filter(subject__contains=searchStr).count()
    #print  'totalCnt=',totalCnt

    pagingHelperIns = pagingHelper();
    totalPageList = pagingHelperIns.getTotalPageList( totalCnt, rowsPerPage)

    # like 구문 적용방법
    #boardList = DjangoBoard.objects.raw("""SELECT Z.* FROM ( SELECT X.*, ceil(rownum / %s) as page \
    #    FROM ( SELECT ID,SUBJECT,NAME, CREATED_DATE, MAIL,MEMO,HITS FROM SAMPLE_BOARD_DJANGOBOARD \
    #    WHERE SUBJECT LIKE '%%'||%s||'%%' ORDER BY ID DESC) X ) Z WHERE page = %s""", [rowsPerPage, searchStr, pageForView])

    boardList = Board.objects.filter(subject__contains=searchStr)
    #print'boardList=',boardList

    return render(request, 'community/listSearchedSpecificPage.html', {'boardList': boardList, 'totalCnt': totalCnt,
                                                        'pageForView':int(pageForView) ,'searchStr':searchStr, 'totalPageList':totalPageList} )

@csrf_exempt
def addComment(request):
    current_page = request.POST['current_page']
    #i = 'memo_id' in request.POST
    br = Comment (cname = User.objects.get(username=request.user.get_username()),
                    comm = request.POST['comm'],
                    memo_id = Board.objects.get(id=request.POST['memo_id']),
                    )
    br.save()

    # 다시 조회
    url = 'viewWork?memo_id='+request.POST['memo_id']+'&current_page='+current_page+'&searchStr=None'
    return HttpResponseRedirect(url)
