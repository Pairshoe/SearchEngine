from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    if request.method == 'GET':
        print(request.GET.get('query'))
    return render(request, 'search/index.html')


def search(request):
    if request.method == 'GET':
        print(request.GET.get('query'))
    return render(request, 'search/result.html')


def detail(request):
    return render(request, 'search/detail.html')


def test(request):
    return render(request, 'search/test.html')
