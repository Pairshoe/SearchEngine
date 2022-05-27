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
        results = searchEngineCore.search_case(0)
        print(results[0])
        for result in results:
            result['highlight'] = ''.join(result['highlight'])
        content['results'] = results
    return HttpResponse(template.render(content, request))


def detail(request):
    template = loader.get_template('search/detail.html')
    if request.method == 'GET':
        print(request.GET.get('id'))
        results = searchEngineCore.get_case(request.GET.get('id'))
        print(results)
    return HttpResponse(template.render(results, request))
