from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from guestbook.models import Guestbook


def index(request): #request 정보를 받아야서 이걸로 값을 얻는다.
    results = Guestbook.objects.all().order_by('-id')
    #print(results,type(results))
    #dics = model_to_dict(results)
    #print(dics, type(dics))
    # count = len(results)
    # for result in results:
    #     result['select'] = count
    #     count -= 1
    data = {'guestbook_list':results}
    #print(data,type(data))
    return render(request, 'guestbook/index.html', data)


def deleteform(request):
    id = request.GET['no']
    data = {"id":id}
    return render(request, 'guestbook/deleteform.html',data)


def insert1(request):
    guestbook = Guestbook()
    guestbook.name = request.POST['name']
    guestbook.password = request.POST['pass']
    guestbook.message = request.POST['content']
    guestbook.save()

    return HttpResponseRedirect("/guestbook")

def delete(request):
    id = request.POST['no']
    password = request.POST['password']
    Guestbook.objects.filter(id=id).filter(password=password).delete()
    return HttpResponseRedirect("/guestbook/")
