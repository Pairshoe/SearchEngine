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
        if request.GET.get('sort_key') is not None:
            sort_key = request.GET.get('sort_key')
        else:
            sort_key = ''
        content['sort_key'] = sort_key
        if request.GET.get('query') is not None:
            searchEngineCore.make_query(request.GET.get('query'), sort_key=sort_key)
            content['query'] = request.GET.get('query')
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
            searchEngineCore.make_query(request.GET.get('keyword'), conditions=condition_list, accurate_mode=True,
                                        sort_key=sort_key)
            content['keyword'] = request.GET.get('keyword')
            content['case_id'] = request.GET.get('case_id')
            content['filing_time'] = request.GET.get('filing_time')
            content['law'] = request.GET.get('law')
            content['law_detailed'] = request.GET.get('law_detailed')
            content['crime'] = request.GET.get('crime')
            content['judge'] = request.GET.get('judge')
            content['court'] = request.GET.get('court')
            content['document_type'] = request.GET.get('document_type')
        else:
            searchEngineCore.make_query(request.GET.get('case_content'), sort_key=sort_key, case_mode=True)
            content['case_content'] = request.GET.get('case_content')

        if request.GET.get('current_page') is not None:
            current_page = int(request.GET.get('current_page'))
            results = searchEngineCore.search_case(current_page)
        else:
            results = searchEngineCore.search_case(1)
            current_page = 1
        content['results'] = results[0]
        content['page_num'] = results[1]
        content['current_page'] = current_page
        content['prev_page'] = current_page - 1
        content['next_page'] = current_page + 1
        content['last_page'] = content['page_num'][-1]
        for result in results[0]:
            result['highlight'] = ''.join(result['highlight'])
    return HttpResponse(template.render(content, request))


def detail(request):
    template = loader.get_template('search/detail.html')
    if request.method == 'GET':
        results = searchEngineCore.get_case(request.GET.get('id'))
        if 100 < len(results['meta']['law']):
            results['meta']['law'] = results['meta']['law'][:100] + '...'
    return HttpResponse(template.render(results, request))


def about(request):
    return render(request, 'search/about.html')
