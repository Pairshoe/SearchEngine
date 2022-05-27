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
        if request.GET.get('query') is not None:
            searchEngineCore.make_query(request.GET.get('query'))
        elif request.GET.get('keyword') is not None:
            condition_list = {
                'case_id': request.GET.get('case_id'),
                'filing_time': request.GET.get('filing_time'),
                'law': request.GET.get('law'),
                'law_detailed': request.GET.get('law_detailed'),
                'crime': request.GET.get('crime'),
                'judge': request.GET.get('judge'),
                'court': request.GET.get('court'),
                'document_type': request.GET.get('document_type'),
            }
            searchEngineCore.make_query(request.GET.get('keyword'), conditions=condition_list)
        else:
            searchEngineCore.make_query(request.GET.get('case_content'))
        results = searchEngineCore.search_case(0)
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
