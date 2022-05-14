from haystack import indexes
from .models import Case


class CaseIndex(indexes.SearchIndex, indexes.Indexable):
    # 以此字段的内容作为索引进行检索
    text = indexes.CharField(document=True, use_template=True, template_name='search/search_text.txt')
    case_number = indexes.CharField(model_attr='case_number')

    def get_model(self):
        return Case
