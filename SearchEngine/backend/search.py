import re, jieba
from elasticsearch import Elasticsearch

TEST = False
INDEX = 'cases_test' if TEST == True else 'cases'


class SearchEngineCore:

    def __init__(self):
        self.es = Elasticsearch('http://localhost:9200')
        self.condition_list = ['case_id', 'filing_time', 'law', 'law_detailed', 'crime', 'judge', 'court',
                               'document_type', 'browse_count']
        self.query = {'bool': {'must': [], 'should': []}}
        self.sort = None
        self.can_search = False

    # content ：用于查询的内容
    # accurate_mode ：精确模式，若开启该模式，将依照空格对搜索词进行分隔并分别精确匹配
    # conditions ：其他搜索条件，包括 condition_list 中列到的所有内容，注意 filing_time 和 browse_count 均为 int 类型，其余为 str
    # sort_key ：排序依据，置空即按照分数排序（默认），还可以选择 filing_time 或 browse_count
    def make_query(self, content: str, accurate_mode: bool = False, case_mode: bool = False, conditions: dict = dict(),
                   sort_key: str = ''):
        assert (sort_key == '' or sort_key == 'filing_time' or sort_key == 'browse_count')
        self.query = {'bool': {'must': [], 'should': []}}
        self.sort = dict()
        content = re.sub(r'[。？！，、；：“”\(\)\{\}\[\]<>（）〔〕【】〖〗《》\-~—…]$', ' ', content)
        if accurate_mode == True:
            for word in content.split():
                self.query['bool']['must'].append({'match_phrase': {'content': word}})
        elif case_mode == True:
            for word in jieba.cut(content, cut_all=True):
                self.query['bool']['should'].append({'match_phrase': {'content': word}})
            self.query['bool']['minimum_should_match'] = '60%'
        else:
            for word in jieba.cut_for_search(content):
                self.query['bool']['should'].append({'match_phrase': {'content': word}})
            self.query['bool']['minimum_should_match'] = '85%'

        for condition in self.condition_list:
            if conditions.get(condition) is not None and conditions[condition] != '':
                if type(conditions[condition]) == str:
                    for word in conditions[condition].split():
                        self.query['bool']['must'].append({'match_phrase': {condition: word}})
                else:
                    self.query['bool']['must'].append({'match_phrase': {condition: conditions[condition]}})

        if sort_key != '':
            self.sort = {sort_key: {'order': 'desc'}}
        else:
            self.sort = None
        self.can_search = True

    def parse_recommend_response(self, response):
        recommends = list()
        for term in response:
            result = {'id': term['_id']}
            for condition in self.condition_list:
                result[condition] = term['_source'][condition]
            result['content_abstract'] = (term['_source']['content'][:300] + '...') if len(
                term['_source']['content']) > 300 else term['_source']['content']
            recommends.append(result)
        return recommends

    # page ：页号
    # 返回结果、页码起始值和页码终止值
    def search_case(self, page: int):
        assert (self.can_search is True)
        results = list()

        response = self.es.search(index=INDEX, from_=(page - 1) * 10, size=10, highlight={'fields': {'content': {}}},
                                  query=self.query, sort=self.sort)
        for term in response['hits']['hits']:
            result = {'id': term['_id']}
            for condition in self.condition_list:
                result[condition] = term['_source'][condition]
            result['highlight'] = term['highlight']['content']
            results.append(result)

        max_page = page
        while max_page < 5 or max_page < page + 2:
            if len(self.es.search(index=INDEX, from_=max_page * 10, size=10, highlight={'fields': {'content': {}}},
                                  query=self.query, sort=self.sort)['hits']['hits']) > 0:
                max_page += 1
            else:
                break

        return results, range(max(max_page - 4, 1), max_page + 1)

    # id ：案件编号
    def get_case(self, id: str):
        try:
            case_detail = self.es.get(index=INDEX, id=id)['_source']
        except:
            return None

        self.es.update(index=INDEX, id=id, doc={'browse_count': case_detail['browse_count'] + 1})
        self.es.indices.refresh(index=INDEX)

        content_raw = case_detail['content'].split()
        title = content_raw[0] + ' ' + content_raw[1]
        content = {'header': list(), 'body': list(), 'judge': list(), 'time': '', 'secretaryn': list(), 'laws': list()}
        counter = 3
        while counter < len(content_raw) and re.search(r'：.*。', content_raw[counter]) is not None:
            content['header'].append(content_raw[counter])
            counter += 1
        while counter < len(content_raw) and (
                re.search(r'[。？！，、；：“”\(\)\{\}\[\]<>（）〔〕【】〖〗《》\-~—…]$', content_raw[counter]) is not None or re.search(
            r'(审判|陪审)', content_raw[counter]) is None):
            content['body'].append(content_raw[counter])
            counter += 1
        while counter < len(content_raw) and re.search(r'[。？！，、；：“”\(\)\{\}\[\]<>（）〔〕【】〖〗《》\-~—…]$',
                                                       content_raw[counter]) is None and re.search(r'(审判|陪审)',
                                                                                                   content_raw[
                                                                                                       counter]) is not None:
            content['judge'].append(content_raw[counter])
            counter += 1
        if counter < len(content_raw) and re.search(r'年.*月.*日.*', content_raw[counter]) is not None:
            content['time'] = content_raw[counter]
            counter += 1
        while counter < len(content_raw) and re.search(r'(书记员|助理)', content_raw[counter]) is not None:
            content['secretaryn'].append(content_raw[counter])
            counter += 1
        while counter < len(content_raw):
            content['laws'].append(content_raw[counter])
            counter += 1

        recommends = list()
        recommend_response = self.es.search(index=INDEX, size=5, query={'match': {'content': (
            case_detail['content'][:5000] if len(case_detail['content']) > 5000 else case_detail['content'])}})
        recommends = self.parse_recommend_response(recommend_response['hits']['hits'])

        query = {'bool': {'must': []}}
        for word in case_detail['judge'].split():
            query['bool']['must'].append({'match_phrase': {'judge': word}})
        recommend_judge_response = self.es.search(index=INDEX, size=5, query=query)
        recommends_judge = self.parse_recommend_response(recommend_judge_response['hits']['hits'])

        query = {'bool': {'must': []}}
        for word in case_detail['law'].split():
            query['bool']['must'].append({'match_phrase': {'law': word}})
        recommend_law_response = self.es.search(index=INDEX, size=5, query=query)
        recommends_law = self.parse_recommend_response(recommend_law_response['hits']['hits'])

        case_detail.pop('content')
        return {'title': title, 'meta': case_detail, 'content': content, 'recommends': recommends,
                'recommends_judge': recommends_judge, 'recommends_law': recommends_law}


if __name__ == '__main__':
    core = SearchEngineCore()
    core.make_query('中华人民共和国刑法', accurate_mode=False)
    print(core.search_case(0))
    print(core.get_case(1))
