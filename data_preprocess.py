import re, os
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch

INDEX = 'cases'


def parse(cont, key):
    res = cont.find(re.compile('.*'), {'namecn': key})
    return res.attrs['value'].strip() if res is not None else ''


def parse_list(cont, key1, key2):
    if key1 != '':
        cont = cont.find(re.compile('.*'), {'namecn': key1})
    res = set()
    if cont is not None:
        for item in cont.find_all(re.compile('.*'), {'namecn': key2}):
            res.add(item.attrs['value'])
    res_str = ''
    for item in res:
        res_str += ' ' + item
    return res_str.strip()


if __name__ == '__main__':
    es = Elasticsearch('http://localhost:9200')
    if es.indices.exists(index=INDEX):
        es.indices.delete(index=INDEX)
    es.indices.create(index=INDEX, mappings={
        "properties": {
            'case_id': { 'type': 'text', 'store': 'true' },
            'filing_time': { 'type': 'integer', 'store': 'true' },
            'law': { 'type': 'text', 'store': 'true' },
            'law_detailed': { 'type': 'text', 'store': 'true' },
            'crime': { 'type': 'text', 'store': 'true' },
            'judge': { 'type': 'text', 'store': 'true' },
            'court': { 'type': 'text', 'store': 'true' },
            'document_type': { 'type': 'text', 'store': 'true' },
            'content': { 'type': 'text', 'store': 'true' },
            'browse_count': {'type': 'integer', 'store': 'true'}
        }
    })
    for _, _, files in os.walk('./raw_data/'):
        for i, file in enumerate(files):
            with open(os.path.join('./raw_data/', file)) as fp:
                cont = BeautifulSoup(fp.read(), 'lxml')
                case_id = parse(cont, '案号')
                filing_time = parse(cont, '立案年度')
                law = parse_list(cont, '法律法条引用', '名称')
                law_detailed = parse_list(cont, '法律法条分组冗余', '法律法条')
                crime = parse_list(cont, '', '完整罪名')
                judge = parse_list(cont, '', '审判人员姓名')
                court = parse(cont, '经办法院')
                document_type = parse(cont, '文书名称')
                try:
                    content = cont.find(re.compile('.*'), {'namecn': '全文'}).attrs['ovalue'].strip()
                    response = es.create(index=INDEX, id=str(i + 1), document={
                        'case_id': case_id,
                        'filing_time': int(filing_time) if filing_time.isnumeric() else 0,
                        'law': law,
                        'law_detailed': law_detailed,
                        'crime': crime,
                        'judge': judge,
                        'court': court,
                        'document_type': document_type,
                        'content': content,
                        'browse_count': 0
                    })
                except AttributeError:
                    print(f'Case {i} has no content, skip.')
            if (i + 1) % 100 == 0:
                print(f'Adding: {i + 1} / {len(files)}')
            # if (i + 1) % 1000 == 0:
            #     break

    es.indices.refresh(index=INDEX)
