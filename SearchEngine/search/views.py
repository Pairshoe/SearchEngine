from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'search/index.html')


def search(request):
    return render(request, 'search/result.html')


def detail(request):
    return render(request, 'search/detail.html')
