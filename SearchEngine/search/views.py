import sys
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from backend.search import SearchEngineCore

sys.path.append("..")
searchEngineCore = SearchEngineCore()


# Create your views here.
def index(request):
    return render(request, 'search/index.html')


def search(request):
    content = {}
    template = loader.get_template('search/result.html')
    if request.method == 'GET':
        searchEngineCore.make_query(request.GET.get('query'))
        results, recommands = searchEngineCore.search_case(0)
        for result in results:
            result['highlight'] = ''.join(result['highlight'])
        content["results"] = results
    return HttpResponse(template.render(content, request))


def detail(request):
    return render(request, 'search/detail.html')


def test(request):
    return render(request, 'search/test.html')
