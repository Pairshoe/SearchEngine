from elasticsearch import Elasticsearch

INDEX = 'cases'


if __name__ == '__main__':
    es = Elasticsearch('http://localhost:9200')
    es.get(index=INDEX, id='68417')
