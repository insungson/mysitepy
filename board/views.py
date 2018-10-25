from django.http import HttpResponseRedirect
from django.shortcuts import render
from board import models
# Create your views here.

def list(request):
    results = models.fetchall()

    count = len(results)
    number = 1
    for result in results:
        result['listnum'] = count
        result['listordernum'] = number
        count -= 1
        number +=1

    print(results[:3]) #이값을 data에 넣고 딕셔너리형태로 만들면 게시판에 원하는 만큼.(시작:끝)슬라이싱


    #print(results,type(results))


    pagesize = 5   #보여질 글 개수

    pagenum = 1    #현재 클릭한 페이지
    if 'pagenum' not in request.GET:
        pagenum = 1
    else:
        pagenum = int(request.GET['pagenum'])

    pageblock = 5  #목록의 갯수(숫자) [1][2][3] 목록이 3개일때

    startpage = 1                       # 처음 게시판들어갈때 페이지
    if pagenum%pageblock == 0:          # 블록의 처음페이지
       startpage = (int(pagenum/pageblock) - 1)*pageblock + 1
    else:
       startpage = int(pagenum/pageblock) * pageblock + 1


    listcount = len(results)
    print(listcount)
    pagecount = 0                       #목록 리스트에 들어갈 총 숫자
    if listcount/pagesize == 0:
        pagecount = int(listcount/pagesize)
    else:
        pagecount = int(listcount/pagesize) + 1

    print(pagecount)

    endpage = startpage + pageblock - 1  # 블록의 끝페이지
    if endpage > pagecount:
        endpage = pagecount


    pagenumber = []                   #목록 리스트의 숫자를 전부 나타내기위함[1][2][3] 이런식의?
    for a in range(1, int(pagecount)+1):
        pagenumber.append(a)
    print(pagenumber)
    for a in pagenumber:
        print(a)

    pagenumber = pagenumber[startpage-1:endpage]    #아래 목록 페이지 슬라이싱으로 끊기

    startrow = (pagenum - 1)*pagesize+1 #시작(첫)행 번호 구하기(글이보여지는 DB저장값의 첫번째 행) 슬라이싱처리
    endrow = pagenum * pagesize    #마지막(끝)행 번호 구하기(글이보여지는 DB저장값의 마지막 행) 슬라이싱처리

    previous_page = endpage-pageblock

    next_page = startpage+pageblock





    page={
        'startpage':startpage,
        'endpage':endpage,
        'pagenum':pagenum,
        'pagecount':pagecount,
        'pageblock':pageblock,
        'previous_page':previous_page,
        'next_page':next_page,
        'pagenumber':pagenumber,
    }
    print(page)

    data = {'board_list': results[startrow-1:endrow], 'page_list': page}
    return render(request, 'board/list.html', data,)


def modifyform(request):
    no = request.GET['no']
    results = models.fetchone(no)
    data = {'board_list': results}
    return render(request, 'board/modify.html', data)

def modify(request):
    no = request.POST['no'] #get은 url을 통해... post는 HTTP바디에 넣어 전송
    title = request.POST['title']
    contents = request.POST['contents']

    models.modifyupdate((title,contents,no))
    return HttpResponseRedirect("/board")

def modifyreply(request):
    no = request.GET['no']
    modi_info = models.modifyreply_info(no)
    print(modi_info,type(modi_info))
    models.update_predata(modi_info)
    data = {'board_list': no}
    return render(request, 'board/modifyreply.html', data)


def modifyreply_write(request):
    title = request.POST['title']
    contents = request.POST['contents']
    no = request.GET['no']
    insert_info = models.findinfo(no)
    print(insert_info,type(insert_info))
    models.insert_modifyreply((title, contents, insert_info[0], insert_info[1]+1, insert_info[2]+1, insert_info[3]))

    return HttpResponseRedirect("/board")


def view(request):
    no = request.GET['no']
    models.hitplus((1,no))
    results = models.fetchone(no)
    data = {'board_list': results}

    return render(request, 'board/view.html', data)


def writeform(request):
    return render(request, 'board/write.html')

def write(request):
    title = request.POST['title']
    contents = request.POST['contents']
    authuser = request.session['authuser']

    models.insert((title, contents, authuser['id']))

    return HttpResponseRedirect("/board")

def delete(request):
    no = request.GET['no']
    models.delete((no))
    return HttpResponseRedirect("/board")


