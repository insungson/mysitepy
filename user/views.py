from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from user.models import User


def joinform(request):
    return render(request, 'user/joinform.html')

def join(request):
    user = User()                      #파이썬에서 객체를 불러오는 법이다.(객체를 user 변수로 받아준다.)
    user.name = request.POST['name']
    user.email = request.POST['email']
    user.password = request.POST['password']
    user.gender = request.POST['gender']
    user.save()
    #models.insert((name,email,password,gender)) #예전버전

    return HttpResponseRedirect('/user/joinsuccess')

def joinsuccess(request):
    return render(request, 'user/joinsuccess.html')

def loginform(request):
    return render(request, 'user/loginform.html')

def login(request):
    # try:
    #     authuser = User.objects.get(email=request.POST['email']).filter(password = request.POST['password'])
    # except User.DoesNotExist:
    #     return return HttpResponseRedirect('/user/loginform?result=fail')
    # ======================================== 윗부분 성모씨꺼보고 고치기

    results = User.objects.filter(email=request.POST['email']).filter(password = request.POST['password'])
    #objects.filter는 전체를 다 가져오지만... get을 쓰면 한줄말 가져오게 된다.
    #user = models.get(email, password)
    #로그인 실패
    if len(results) is None:
        return HttpResponseRedirect('/user/loginform?result=fail')

    #로그인 성공시(처리)
    authuser = results[0]
    print(authuser)
    request.session['authuser'] = model_to_dict(authuser)
    #model_to_dict 는 딕셔너리 형태로 집어넣는다.딕셔너리로 넣어야 에러가 안난다.
    #세션에 저장해놓으면 쿠키가 지워지지 않는 이상 같은 값이 들어와도 있다.
    #main으로 리다이렉트
    return HttpResponseRedirect('/')

def logout(request):
    print(request.session['authuser'])
    del request.session['authuser']
    return HttpResponseRedirect('/')

def modifyform(request):
    authuser = request.session['authuser']
    data={'user':authuser}
    return render(request,'user/modifyform.html',data)

def checkemail(request):
    results = User.objects.filter(email = request.GET['email'])

    result = {'result':len(results) == 0}   #true면 not exist[사용가능]
    return JsonResponse(result)

def modify(request):
    dict_user = request.session['authuser']
    print(dict_user)
    changeuser = User.objects.filter(id=dict_user['id'])
    user = changeuser[0]
    user.password = request.POST['password']
    user.gender = request.POST['gender']
    user.save()

    newuser = User.objects.filter(id=dict_user['id'])
    authuser = newuser[0]
    request.session['changeuser'] = model_to_dict(authuser)



    # changeuser = User.objects.filter(email=request.POST['email']).filter(name=request.POST['name'])
    # authuser = changeuser[0]
    # authuser.password = request.POST['password']
    # authuser.gender = request.POST['gender']
    # authuser.save()


    return HttpResponseRedirect('/')
