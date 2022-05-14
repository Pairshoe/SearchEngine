import datetime
from django.db import models


# Create your models here.
class Case(models.Model):
    # 全文
    context = models.TextField()
    # 经办法院
    # 法院级别
    # 行政区划（省）
    # 行政区划（市）
    # 案号
    case_number = models.CharField(max_length=100)
    # 案件类别
    # 审判程序
    # 相关法律条文

    def __str__(self):
        return self.case_number
